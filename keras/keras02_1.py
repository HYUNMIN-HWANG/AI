"""
(암묵적인) 네이밍 룰
JAVA : 카멜케이스 - 의미가 시작되는 부분이 대문자로 시작함
python : 의미가 시작되는 부분에 _(언더바)로 구분한다.
"""
# x >> x_train, x_test



#import는 통상적으로 맨 위에 몰아서 넣어준다.
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential
#[2] from tensorflow.keras import models
#[3] from tensorflow import keras

from tensorflow.keras.layers import Dense


#1. Data 
#원래의 데이터를 훈련시키는 데이터와 평가 데이터를 구분한다. 실질적인 데이터는 "1,2,3,4,5,6,7,8" >> 을 둘로 나눈 것
x_train = np.array([1,2,3,4,5])
y_train = np.array([1,2,3,4,5])

x_test = np.array([6,7,8])
y_test = np.array([6,7,8])

#2. Model
model = Sequential()
#[2] model = models.Sequential()
#[3] model = keras.models.Sequential()

model.add(Dense(50000, input_dim=1, activation='relu'))
model.add(Dense(1000))     #activation을 적지 않는다면, default 값(=linear)적용된다.
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(100))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(10))
model.add(Dense(1)) # output = 1

#3. Compile, Train
model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=100, batch_size=1)

#4. evaluate, predict
loss = model.evaluate(x_test, y_test, batch_size=1)
print('loss : ', loss)

result = model.predict([9])
print("result : ", result)