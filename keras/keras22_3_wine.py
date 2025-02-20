# wine 
# DNN 모델을 완성할 것
import numpy as np
from sklearn.datasets import load_wine

dataset = load_wine()

# print(dataset.DESCR)
# print(dataset.feature_names)

# ['alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', \
# 'magnesium', 'total_phenols', 'flavanoids', 'nonflavanoid_phenols', \
# 'proanthocyanins', 'color_intensity', 'hue', 'od280/od315_of_diluted_wines', 'proline']

#1. DATA

x = dataset.data
y = dataset.target

# print(x)        # preprocessing 해야 함
# print(y)        # 0, 1, 2 >> 다중분류
# print(x.shape)  # (178, 13)
# print(y.shape)  # (178, )

# x > preprocessing
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, shuffle=True, random_state=55)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

print(x_train.shape)    # (160, 13)
print(x_test.shape)     # (18, 13)

# y > preprocessing
from tensorflow.keras.utils import to_categorical

y_train = to_categorical(y_train) 
y_test = to_categorical(y_test)
print(y_train.shape)    # (160, 3)
print(y_test.shape)     # (18, 3)

#2. Modeling
#2. Modeling
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(65, activation='relu', input_shape=(13,)))  # input = 13
model.add(Dense(65, activation='relu'))
model.add(Dense(39, activation='relu'))    
model.add(Dense(39, activation='relu'))    
model.add(Dense(13, activation='relu'))      
model.add(Dense(3, activation='softmax'))                   # output = 3

model.summary()

#3. Compile, Train
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', 'mae'])  # 다중 분류 : categorical_crossentropy 
from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss', patience=5, mode='min') 
model.fit(x_train, y_train, epochs=45, batch_size=13, validation_split=0.1, verbose=1,callbacks=[early_stopping])

#4. Evalutate Predcit
loss, acc, mae = model.evaluate(x_test, y_test, batch_size=13)
print("loss : ",loss)
print("accuracy : ", acc)
print("mae : ", mae)

# print(x_test[-5:-1])
y_predict = model.predict(x_test[-5:-1])

print("y_test_data :\n", y_test[-5 : -1])
print("y_predict :\n", y_predict)

print("result : ", np.argmax(y_predict,axis=1))

# Dense
# loss :  0.023476235568523407
# accuracy :  1.0
# mae :  0.013629034161567688
# y_test_data :
#  [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]
#  [1. 0. 0.]]
# y_predict :
#  [[9.9991262e-01 5.4553703e-07 8.6745582e-05]
#  [4.8492066e-06 9.9999499e-01 7.3400358e-08]
#  [4.3661150e-04 2.8053637e-05 9.9953532e-01]
#  [9.9972695e-01 2.6720166e-04 5.8833466e-06]]
# result :  [0 1 2 0]