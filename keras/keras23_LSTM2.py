# input_shape >>> input_length / input_dim

# RNN > LSTM (x 데이터를 2차원에서 3차원으로 만들어줘야 함)

#1. DATA
import numpy as np

x = np.array([[1,2,3],[2,3,4],[3,4,5],[4,5,6]])
y = np.array([4,5,6,7])

print("x.shape : ", x.shape)  #(4, 3)
print("y.shape : ", y.shape)  #(4, )

# LSTM을 사용해서 계산하기 위해서 x 모양을 변경  >> ***3차원 데이터로 만들어준다.***
# 행 / 렬 / 몇 개씩 자르는지 (batch_size / time_steps / input_dim)
# 1개 데이터 씩 잘라서 3개를 계산해서 y 결과값 낸다.
# 데이터 자체의 손실 없음, 내용 변경 없음
x = x.reshape(4, 3, 1)        
# print(x)                    # [[[1],[2],[3]], [[2],[3],[4]], [[3],[4],[5]], [[4],[5] [6]]]


#2. Modeling
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

model = Sequential()
# model.add(LSTM(10, activation='relu', input_shape=(3,1)))   # x : 행을 무시한 데이터를 인풋
model.add(LSTM(10, activation='relu', input_length=3, input_dim=1))   #input_shape 대신 input_dim 사용
model.add(Dense(20))
model.add(Dense(10))
model.add(Dense(1))

# model.summary()

"""
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
lstm (LSTM)                  (None, 10)                480          <- 4 X (input_dim + bias(1) + output) X output
_________________________________________________________________
dense (Dense)                (None, 20)                220
_________________________________________________________________
dense_1 (Dense)              (None, 10)                210
_________________________________________________________________
dense_2 (Dense)              (None, 1)                 11
=================================================================
Total params: 921
Trainable params: 921
Non-trainable params: 0
_________________________________________________________________
"""

#3. Compile, Train
model.compile(loss='mse', optimizer='adam')
model.fit(x, y, epochs=100, batch_size=1)

#4. Evaluate, Predict
loss = model.evaluate(x, y)
print(loss)

x_pred = np.array([5,6,7])          # (3, )
x_pred = x_pred.reshape(1, 3, 1)    # LSTM에 쓸 수 있는 3차원 데이터로 만들어준다

result = model.predict(x_pred)
print(result)                       # 결과값 8 예상


# 0.01419631764292717
# [[7.8094993]]