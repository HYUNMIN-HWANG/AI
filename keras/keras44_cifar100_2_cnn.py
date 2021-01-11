# cifar100 (컬러)

from tensorflow.keras.datasets import cifar100
import matplotlib.pyplot as plt
import numpy as np

#1. DATA 
(x_train, y_train), (x_test, y_test) = cifar100.load_data()
print(x_train.shape, y_train.shape) # (50000, 32, 32, 3) (50000, 1)
print(x_test.shape, y_test.shape)   # (10000, 32, 32, 3) (10000, 1)

# print(x_train[0])   
# print("y_train[0] : " , y_train[0])   # 19
# print(x_train[0].shape)               # (32, 32, 3)

# plt.imshow(x_train[0])        # 0 : black, ~255 : white (가로 세로 색깔)
# # plt.imshow(x_train[0]) # 색깔 지정 안해도 나오긴 함
# plt.show()  

# x > preprocessing
x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],x_train.shape[2],x_train.shape[3]) / 255.
x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],x_test.shape[2],x_test.shape[3]) / 255.
# print(x_train.shape)    # (50000, 32, 32, 3)

# y > preprocessing
from tensorflow.keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

#2. Modeling
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPool2D

model = Sequential()
model.add(Conv2D(filters=100, kernel_size=(2,2),padding='same',input_shape=(x_train.shape[1],x_train.shape[2],x_train.shape[3])))
model.add(Dropout(0.2))
model.add(MaxPool2D(pool_size=2))
model.add(Conv2D(filters=100,kernel_size=(2,2)))
model.add(Dropout(0.2))
model.add(Conv2D(filters=50,kernel_size=(2,2)))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(50))
model.add(Dense(100,activation='softmax'))

# model.summary()

#3. Compile, Train
from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='loss', patience=10, mode='min')

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['acc'])
model.fit(x_train, y_train, epochs=100, batch_size=32,validation_split=0.2, verbose=1, callbacks=[es])
# model.fit(x_train, y_train, epochs=100, batch_size=32,validation_split=0.2, verbose=1)

#4. predict, Evaluate
loss, acc = model.evaluate(x_test, y_test, batch_size=32)
print("loss : ", loss)
print("acc : ", acc)

print("y_test : ", np.argmax(y_test[-5:-1],axis=1))
y_pred = model.predict(x_test[-5:-1])
print("y_pred : ", np.argmax(y_pred,axis=1))

# CNN
# loss :  4.324522018432617
# acc :  0.2232999950647354
# y_test :  [83 14 51 42]
# y_pred :  [88 80 51 44]