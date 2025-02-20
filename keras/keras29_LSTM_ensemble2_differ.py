# 2개의 모델 중 하나는 LSTM, 하나는 Dense로 앙상블 구현
# 29_LSTM_1와 성능비교

import numpy as np

#1. DATA
x1 = np.array([[1,2,3],[2,3,4],[3,4,5],[4,5,6],
                [5,6,7],[6,7,8],[7,8,9],[8,9,10],
                [9,10,11],[10,11,12],
                [20,30,40],[30,40,50],[40,50,60]])
x2 = np.array([[10,11,12],[20,30,40],[30,40,50],[40,50,60],
                [50,60,70],[60,70,80],[70,80,90],[80,90,100],
                [90,100,110],[100,110,120],
                [2,3,4],[3,4,5],[4,5,6]])
y = np.array([4,5,6,7,8,9,10,11,12,13,50,60,70]) 
x1_predict = np.array([55,65,75])
x2_predict = np.array([65,75,85])

# print(x1.shape)            # (13, 3)
# print(y.shape)             # (13, )
# print(x1_predict.shape)    # (3,) -> Dense (1, 3) -> LSTM (1, 3, 1)

# 생각할 점 >> x1, x2 동일한 데이터 수가 다를 수 있다. (ex. 1년치 데이터 vs 2년치 데이터) 

x1_predict = x1_predict.reshape(1, 3)
x2_predict = x2_predict.reshape(1, 3)

# preprocessing

from sklearn.model_selection import train_test_split
x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y, train_size=0.9, shuffle=True, random_state=44)  
x2_train, x2_test = train_test_split(x2, train_size=0.9, shuffle=True, random_state=44)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x1_train)
scaler.fit(x2_train)
x1_train = scaler.transform(x1_train)
x2_train = scaler.transform(x2_train)
x1_test = scaler.transform(x1_test)
x2_test = scaler.transform(x2_test)
x1_predict = scaler.transform(x1_predict)
x2_predict = scaler.transform(x2_predict)

# print(x1_train.shape)             # (11, 3)
# print(x1_test.shape)              # (2, 3)

# *** LSTM 모델을 사용하기 위해서 데이터를 3차원으로 만들어준다. ***
# x1_train = x1_train.reshape(11, 3, 1)
# x2_train = x2_train.reshape(11, 3, 1)

x1_train = x1_train.reshape(x1_train.shape[0],x1_train.shape[1], 1 )
x2_train = x2_train.reshape(x2_train.shape[0],x2_train.shape[1], 1 )

x1_test = x1_test.reshape(2, 3, 1)
x2_test = x2_test.reshape(2, 3, 1)

x1_predict = x1_predict.reshape(1, 3, 1)
x2_predict = x2_predict.reshape(1, 3, 1)

#2. Modeling
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input, LSTM

# 모델 구성
# (1) model1 - LSTM / model2 - Dense

input1 = Input(shape=(3,1))
dense1 = LSTM(65, activation='relu')(input1)
dense1 = Dense(13, activation='relu')(dense1)

input2 = Input(shape=(3,))
dense2 = Dense(65, activation='relu')(input2)
dense2 = Dense(13, activation='relu')(dense2)

# (2) model1 - Dense / model2 - LSTM

# input1 = Input(shape=(3,))
# dense1 = Dense(65, activation='relu')(input1)
# dense1 = Dense(13, activation='relu')(dense1)

# input2 = Input(shape=(3,1))
# dense2 = LSTM(65, activation='relu')(input2)
# dense2 = Dense(13, activation='relu')(dense2)

# 모델 병합 : concatenate
from tensorflow.keras.layers import concatenate
merge1 = concatenate([dense1, dense2]) 
middle1 = Dense(39)(merge1)
middle1 = Dense(13)(middle1)

# 모델 분기
# model 1
output1 = Dense(39)(middle1)
output1 = Dense(1)(output1) # 최종 output = 1

# 모델 선언
model = Model(inputs=[input1, input2], outputs=output1)

# model.summary()

#3. Compile, Train
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss',patience=10,mode='min')
model.fit([x1_train,x2_train], y1_train, epochs=2600, batch_size=5, validation_split=0.1, callbacks=[early_stopping])

#4. Evaluate, Predict
loss = model.evaluate([x1_test,x2_test], y1_test, batch_size=1)
print("loss, mae : ", loss)

y_pred = model.predict([x1_predict,x2_predict])

print("y_pred1 : ", y_pred)

# 둘 다 LSTM
# loss, mae :  [0.37576156854629517, 0.4345831871032715]
# y_pred1 :  [[77.25795]]

# model1 - LSTM / model2 - Dense
# loss, mae :  [8.484634399414062, 2.071232318878174]
# y_pred1 :  [[80.485794]]

# model1 - Dense / model2 - LSTM
# loss, mae :  [2.898270845413208, 1.2140560150146484]
# y_pred1 :  [[79.92602]]