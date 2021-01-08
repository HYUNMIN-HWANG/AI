# Dropout
# model.add(Dropout(0.2))
# Dropout 하기 전과 성능 비교

import numpy as np
from sklearn.datasets import load_iris

#1. DATA
# x, y, = load_iris(return_X_y=True) # x와 y를 분리하는 방법
# 아래 3 줄과 동일함
dataset = load_iris()
x = dataset.data 
y = dataset.target 

# print(dataset.DESCR)
# print(dataset.feature_names)
# ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

# print(x.shape)  #(150, 4)
# print(y.shape)  #(150, )
# print(x[:5])
# print(y)        # 나올 수 있는 경우의 수 3가지 : 0 , 1 , 2 (50개 씩) >>> 다중 분류 >>> 원핫인코딩해야 함

# x값 전처리
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, shuffle=True, random_state=66)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# 다중 분류일 때, y값 전처리 One hot Encoding (1) tensorflow.keras 사용
from tensorflow.keras.utils import to_categorical
# from keras.utils.np_utils import to_categorical # 옛날 버전

y_train = to_categorical(y_train) 
y_test = to_categorical(y_test)
# print(y_train)
# print(y_test)
print(y_train.shape)    # (120, 3) >>> output = 3
print(y_test.shape)     # (30, 3)

# 다중 분류일 때, y값 전처리 One hot Encoding (2) sklearn 사용 >>> keras22_1_iris1_(2)skelarn.py

#2. Modeling
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential()
model.add(Dense(16, activation='relu', input_shape=(4,)))   #input = 4
model.add(Dropout(0.2))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))                  
            # output = 3 (다중분류모델에서는 분류하는 수만큼 노드개수를 정한다.)                           
            # softmax : 마지막 노드를 다 합치면 1이 된다. > 그 중에서 가장 큰 값이 선택된다.

#3. Compile, Train
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc','mae'])  # acc == accuracy
from tensorflow.keras.callbacks import EarlyStopping
early_stopping = EarlyStopping(monitor='loss', patience=20, mode='min') 
model.fit(x_train, y_train, epochs=300, batch_size=5, validation_split=0.2, verbose=1,callbacks=[early_stopping])


#4. Evaluate, Predict
loss, acc, mae  = model.evaluate(x_test, y_test,batch_size=5)
print("loss : ", loss)
print("accuracy : ", acc)
print("mae : ", mae)

y_predict = model.predict(x_test[-5:-1])
print("y_data :\n", y_test[-5 : -1])
print("y_predict :\n", y_predict)   
# 결과가 0,1,2가 아닌 소수가 나온다. >> softmax : 분류하고자 하는 숫자의 개수만큼 값이 분리된다. 다 합하면 1
# 원하는 결과가 나오도록 0,1,2로 정제해야 함 >> argmax

# y값 중에서 가장 큰 값이 있는 위치를 반환해줌
# argmax - 0은 열(column), 1은 행(row), 2는 면(page, 행열)
print(np.argmax(y_predict,axis=1))


# 원핫인코딩 한 후
# loss :  0.05020342767238617
# accuracy :  1.0
# mae :  0.0286836139857769
# y_data :
#  [[0. 0. 1.]
#  [1. 0. 0.]
#  [1. 0. 0.]
#  [0. 0. 1.]]
# y_predict :
#  [[2.2208088e-15 2.0895617e-04 9.9979109e-01]
#  [9.9998808e-01 1.1910735e-05 1.0679650e-27]
#  [9.8897481e-01 1.1025138e-02 1.3339521e-15]
#  [1.0321673e-08 3.9325234e-01 6.0674769e-01]]
# [2 0 0 2]

# Dropout (성능 떨어짐. 드랍아웃하기에는 노드 수가 적다.)
# loss :  0.12442982941865921
# accuracy :  0.9666666388511658
# mae :  0.06698165833950043
# y_data :
#  [[0. 0. 1.]
#  [1. 0. 0.]
#  [1. 0. 0.]
#  [0. 0. 1.]]
# y_predict :
#  [[3.3452940e-09 4.5994428e-04 9.9954009e-01]
#  [9.9998748e-01 1.1842724e-05 6.5958801e-07]
#  [9.9688739e-01 2.8875351e-03 2.2504656e-04]
#  [5.1011174e-04 6.4907956e-01 3.5041034e-01]]
# [2 0 0 1]