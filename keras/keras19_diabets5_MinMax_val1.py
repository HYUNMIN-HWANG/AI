# 당뇨병 회귀모델
# 실습 : 18에서 했던 것과 동일하게 19-1,2,3,4,5, EarlyStopping 까지 총 6개의 파일을 완성하시오.

# [4] x_train 데이터만 전처리 한다.
# validation data

import numpy as np
from sklearn.datasets import load_diabetes

dataset = load_diabetes()

#1. DATA
x = dataset.data
y = dataset.target

print(x[:5])
print(y[:10])

print(x.shape, y.shape)         #(442, 10) (442,) input = 10, output = 1

print(np.max(x), np.min(y))     # 0.198787989657293 25.0  ---> 전처리 해야 함
print(np.max(x), np.min(x))     # 0.198787989657293 -0.137767225690012
print(dataset.feature_names)    # 10 column
                                # ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
# print(dataset.DESCR)

# 전처리 과정
# x = x/0.198787989657293

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=66)
x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, train_size=0.8, shuffle=True, random_state=66)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)     
x_test = scaler.transform(x_test)
x_validation = scaler.transform(x_validation)


#2. Modeling
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()
model.add(Dense(128, input_shape=(10,), activation='relu'))
model.add(Dense(64))
model.add(Dense(64))
model.add(Dense(64))
model.add(Dense(32))
model.add(Dense(32))
model.add(Dense(32))
model.add(Dense(1))

#3. Compile, Train
model.compile(loss='mse', optimizer='adam',metrics=['mae'] )
model.fit(x_train, y_train, epochs=2000, batch_size=6, validation_data=(x_validation, y_validation), verbose=1)

#4. Evaluate, Predict
loss, mae = model.evaluate(x_test, y_test, batch_size=6)
print("loss : ", loss)
print("mae : ", mae)

y_predict = model.predict(x_test)

# RMSE
from sklearn.metrics import mean_squared_error
def RMSE (y_test, y_predict) :
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE : ", RMSE(y_test, y_predict))

# R2
from sklearn.metrics import r2_score
r2 = r2_score (y_test, y_predict)
print("R2 : ", r2)

# 전처리 전
# loss :  4666.92919921875
# mae :  52.11721420288086
# RMSE :  68.31492531690576
# R2 :  0.31249270445756727

# 전처리 후 (전체 x)
# loss :  4415.61376953125
# mae :  51.35456848144531
# RMSE :  66.4500844041374
# R2 :  0.19858893084380513

# MinMaxscler 전처리 후 
# loss :  3455.354248046875
# mae :  46.128021240234375
# RMSE :  58.78226050631079
# R2 :  0.36575261138882453


# x_train 만 MinMaxScaler 전처리 후 (validation_split)
# loss :  4511.89453125
# mae :  50.58407211303711
# RMSE :  67.17063568731487
# R2 :  0.2168597888988395

# x_train 만 MinMaxScaler 전처리 후 (validation_data)
# loss :  4529.0439453125
# mae :  52.34434127807617
# RMSE :  67.29817427871185
# R2 :  0.03891388103623972