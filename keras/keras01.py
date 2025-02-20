#deep learning 기초 모델
#1. 데이터 준비 #2. 모델구성 #3. 컴파일 & 훈련 #4. 평가 & 예측

import numpy as np
import tensorflow as tf 

#1. (정제된) 데이터 준비
x = np.array([1,2,3])
y = np.array([1,2,3])

#2. 모델구성
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense # y=ax+b를 구성하는 가장 기본 

model = Sequential() #순차적인 모델을 만들 것이다. #윗단의 아웃풋은 아래의 인풋이 됨
model.add(Dense(5, input_dim=1, activation='linear')) # add 모델을 더해나간다. (노드 개수 아웃풋 다섯개 , 인풋 한 개, 선형)
model.add(Dense(3, activation='linear'))   #(위 레이어 노드가 인풋이 된다.)
model.add(Dense(4))
model.add(Dense(1)) #최종 아웃풋 1개

#3. 컴파일 & 훈련
model.compile(loss = 'mse', optimizer='adam') #머신이 이해할 수 있도록 컴파일 
            #loss가 작은 걸 기준으로 mse(평균 제곱 오차) 잡는다 / 최적화 adam을 사용한다  / 최적의 weight를 구할 것임(=최소의 loss값)
model.fit(x, y, epochs= 1000, batch_size=1)  #정제된 데이터를 훈련시킨다. 
            # epochs : 훈련을 1000번 시킨다. / batch_size : 몇 단 씩 잘라서 훈련시킬 것인가.

#4. 평가, 예측
loss = model.evaluate(x, y, batch_size=1) #loss값이 작을 수록 좋은 것 (단점 : 평가하는 데이터와 훈련시키는 데이터를 구분할 수 없다. >> keras02.py )
print('loss : ', loss)  

x_pred = np.array([4])
result = model.predict(x_pred) #우리의 최종 목표 : 예측하기
#result = model.predict([4]) #predict 안에는 예측하고 싶은 값을 넣는다.
print('result : ', result)
