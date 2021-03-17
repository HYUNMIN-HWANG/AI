import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from sklearn.model_selection import train_test_split, KFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline
import cv2 as cv
from glob import glob
import matplotlib.pyplot as plt
import os
from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.applications.efficientnet import preprocess_input
import pandas as pd
from tensorflow.keras.layers import Dense, Flatten, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

########### npy save

train_datagen = ImageDataGenerator(
    # rescale=1./255,
    width_shift_range=(-1,1),
    height_shift_range=(-1,1),
    rotation_range=5,
    zoom_range=5,
    shear_range=0.5,
    fill_mode='nearest'
)

# test_datagen = ImageDataGenerator(rescale=1./255)


# xy_data = train_datagen.flow_from_directory(
#     '../data/LPD_competition/train',
#     target_size=(128, 128),
#     batch_size=50000,
#     class_mode='categorical'
# )   # Found 48000 images belonging to 1000 classes.

# print(xy_data)  # <tensorflow.python.keras.preprocessing.image.DirectoryIterator object at 0x00000299B4548550>
# print(xy_data[0][0].shape)  # x (48000, 128, 128, 3)
# print(xy_data[0][1].shape)  # y (48000, 10000)


# np.save('../data/LPD_competition/npy/data_x1.npy', arr=xy_data[0][0])
# np.save('../data/LPD_competition/npy/data_y1.npy', arr=xy_data[0][1])

########### npy load

#1. DATA
x_data = np.load('../data/LPD_competition/npy/data_x1.npy')
y_data = np.load('../data/LPD_competition/npy/data_y1.npy')

print(x_data.shape, y_data.shape)   # (48000, 128, 128, 3) (48000, 1000)

x_data = preprocess_input(x_data)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.8, shuffle=True, random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, train_size=0.8, shuffle=True, random_state=42)
print(x_train.shape, x_test.shape, x_val.shape)  # (30720, 128, 128, 3) (9600, 128, 128, 3) (7680, 128, 128, 3)
print(y_train.shape, y_test.shape, y_val.shape)  # (30720, 1000) (9600, 1000) (7680, 1000)

# kf = KFold(n_splits=8, shuffle=True, random_state=42)


#2. Modeling
def my_model() :
    b7 = EfficientNetB7(weights='imagenet', include_top=False, input_shape=(128, 128,3))
    b7.trainable = False
    model = Sequential()
    model.add(b7)
    model.add(GlobalAveragePooling2D())
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1000, activation='softmax'))
    return model


es = EarlyStopping(monitor='val_loss', patience=20, mode='min')
lr = ReduceLROnPlateau(monitor='val_loss', patience=10, factor=0.4)
path = '../data/LPD_competition/cp/cp_0317_2_b7.hdf5'
cp = ModelCheckpoint(path, monitor='val_loss', save_best_only=True, mode='min')

model = my_model()
model.summary()

batch = 16

model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=1e-5,epsilon=None), metrics=['acc'])
model.fit(x_train, y_train, epochs=100, batch_size=batch , steps_per_epoch=len(x_train)//batch,\
    validation_data=(x_val, y_val), callbacks=[es, lr, cp])

result = model.evaluate(x_test, y_test, batch_size=batch)
print("loss ", result[0])
print("acc ", result[1])


#4. Predict
submission = pd.read_csv('../data/LPD_competition/sample.csv', index_col=0)
# print(submission.shape) # (72000, 2)

test_image = glob('../data/LPD_competition/test/*.jpg')
# print(len(test_image))      # 72000

model = load_model('../data/LPD_competition/cp/cp_0317_2_b7.hdf5')  # all 718

# model.summary()

for img in test_image :
    now_img = os.path.basename(img)
    print("\n", now_img)

    copy_img = img 
    img1 = load_img(copy_img , color_mode='rgb', target_size=(128,128)) 
    img1 = img1.resize((128, 128))
    img1 = np.array(img1)/255.
    img1 = img1.reshape(-1, 128, 128,3)
    # print(img1.shape)   # (1, 128, 128, 3)
    pred = np.argmax(model.predict(img1))

    print(pred)

    submission.loc[now_img,:] = pred
    # print(submission.head())

submission.to_csv('../data/LPD_competition/sub_0317_2.csv', index=True)
