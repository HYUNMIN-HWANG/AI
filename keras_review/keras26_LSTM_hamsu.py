# keras23_LSTM3_sclae 을 함수형으로
# 실습 LSTM (예측값이 80이 나오도록 코딩하여라)

import numpy as np
#1. DATA
x = np.array([[1,2,3],[2,3,4],[3,4,5],[4,5,6],
                [5,6,7],[6,7,8],[7,8,9],[8,9,10],
                [9,10,11],[10,11,12],
                [20,30,40],[30,40,50],[40,50,60]])
y = np.array([4,5,6,7,8,9,10,11,12,13,50,60,70])

print(x.shape)  #(13, 3)
print(y.shape)  #(13, )

x_pred = np.array([50,60,70])   # 목표 예상값 80
x_pred = x_pred.reshape(1, 3)

# 전처리
# LSTM에서 Minmaxscaler : 
# Minmaxscaler는 3차원을 처리할 수 없기 때문에 전처리를 한 후에 3차원으로 reshape를 한다.

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, shuffle=True, random_state=88)  

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)
x_pred = scaler.transform(x_pred)

print(x_train.shape)    #(11, 3)
print(x_test.shape)     #(2, 3)

x_train = x_train.reshape(11, 3, 1)
x_test = x_test.reshape(2, 3, 1)
x_pred = x_pred.reshape(1, 3, 1)

#2. Modeling
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, LSTM

input1 = Input(shape=(3,1))
dense1 = LSTM(65, activation='relu')(input1)
dense1 = Dense(52)(dense1)
dense1 = Dense(52)(dense1)
dense1 = Dense(26)(dense1)
dense1 = Dense(13)(dense1)
output1 = Dense(1)(dense1)

model = Model(inputs=input1, outputs=output1)
# model.summary()

#3. Compile.Train
model.compile(loss = 'mse', optimizer='adam', metrics=['mae'])

from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss', patience=20, mode='min')
model.fit(x_train, y_train, epochs= 2600, batch_size=6, validation_split=0.1, verbose=1, callbacks=[early_stopping])

#3. Evaluate, Predcit
loss, mae = model.evaluate(x_test,y_test,batch_size=3)
print("loss : ", loss)
print("mae : ", mae)

y_pred = model.predict(x_pred)
print("y_pred : ", y_pred)

# LSTM (405번)
# loss :  0.0009525410714559257
# mae :  0.030837297439575195
# y_pred :  [[79.593445]]

# Dense (2600번)
# loss :  0.0005297368043102324
# mae :  0.02149200439453125
# y_pred :  [[80.04368]]
