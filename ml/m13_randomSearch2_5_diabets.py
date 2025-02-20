# gridSearch 단점 : 너무 느리다. 파라미터 100프로 모두 돌린다. 내가 지정한 파라미터를 100프로 신뢰할 수 없다.
# >> randomSearch : 
# >> RandomizedSearchCV : 모든 파라미터를 건드릴 필요가 없다. 랜덤하게 일부만 확인한다. 속도가 빠르다.


import numpy as np
from sklearn.datasets import load_diabetes

from sklearn.preprocessing import MinMaxScaler, StandardScaler  # 둘 중에 하나 사용
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score, r2_score

# 모델마다 나오는 결과 값을 비교한다.
# from sklearn.linear_model import LinearRegression
# from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor  # Regressor : 회귀모델
# from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

import warnings
warnings.filterwarnings('ignore')

import datetime 

########################################################

#1. DATA
dataset = load_diabetes()
x = dataset.data 
y = dataset.target 

# preprocessing >>  K-Fold 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=44)

kfold = KFold(n_splits=5, shuffle=True) # 데이터를 5등분한다. > train data 와 test data 로 구분한다.

# dictionary 3개 (key-value 쌍) - SVC parameters에 해당하는 값들
parameters=[
    {'n_estimators' : [100, 200, 300, 400], 'max_depth' : [6, 8, 10], 'n_jobs' : [-1, 2, 4]},
    {'max_depth' : [6, 8, 10, 12, 14], 'min_samples_leaf' : [3, 7, 9, 12]},
    {'min_samples_leaf' : [3, 5, 7, 9, 10], 'min_samples_split' : [2, 5, 10]},
    {'min_samples_split' : [2, 3, 5, 9, 10], 'n_jobs' : [-1, 2, 4]}
]

#2. Modeling 
# model = SVC()
model = RandomizedSearchCV(RandomForestRegressor(), parameters, cv=kfold)
# 모델 : RandomForestClassifier()
# parameters : SVC에 들어가 있는 파라미터 값들 (딕셔너리 형태)
# cv=kfold : 5번 돌리겠다.
# 총 90번 모델이 돌아감


#3. Compile, Train
start = datetime.datetime.now()
model.fit(x_train, y_train)
end = datetime.datetime.now()
print("time : ", end - start)   # time :  0:00:14.249237

#4. Evaluate, Predict
print("최적의 매개변수 : ", model.best_estimator_)
#  model.best_estimator_ : GridSearchCV에서 90번 돌린 것 중에서 어떤 파라미터가 가장 좋은 값인지 알려준다.

y_pred = model.predict(x_test)
print('최종정답률', r2_score(y_test, y_pred))

aaa = model.score(x_test, y_test)
print('aaa ', aaa)

# GridSearch
# 최적의 매개변수 :  RandomForestRegressor(max_depth=12, min_samples_leaf=10)
# 최종정답률 0.4838812611290275
# aaa  0.4838812611290275

# RandomSearch
# 최적의 매개변수 :  RandomForestRegressor(min_samples_leaf=10, min_samples_split=10)
# 최종정답률 0.47678641072030825
# aaa  0.47678641072030825
