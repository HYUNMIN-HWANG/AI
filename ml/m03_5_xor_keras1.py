# XOR 해결
# 딥러닝 acc :  0.75
# accuracy_score    # 정확도

from sklearn.svm import LinearSVC, SVC
import numpy as np
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

#1. DATA (XOR)
x_data = [[0,0], [1,0], [0,1], [1,1]]
y_data = [0, 1, 1, 0]

#2. Modeling
# model = LinearSVC()
# model = SVC()

model = Sequential()
model.add(Dense(1, input_dim=2, activation='sigmoid'))


#3. Compile, Train
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
model.fit(x_data, y_data, batch_size=1, epochs=100)


#4. evaluate, Predict

y_pred = model.predict(x_data)      
print(x_data, "의 예측결과 : \n", y_pred)   # [[0, 0], [1, 0], [0, 1], [1, 1]] 의 예측결과 :  [0 1 1 0]

result = model.evaluate(x_data, y_data)    
print("model.evaluate : ", result[1])      # acc :  0.75

# acc = accuracy_score(y_data, y_pred)
# print("accuracy_score : ", acc)         # accuracy_score : 1.0