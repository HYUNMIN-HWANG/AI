# 실습 : RandomizedSearch, GridSearch와 Pipeline를 엮는다.
# 모델 : RandomForest

import numpy as np
from sklearn.datasets import load_diabetes

from sklearn.preprocessing import MinMaxScaler, StandardScaler  # 둘 중에 하나 사용
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline, make_pipeline

# 모델마다 나오는 결과 값을 비교한다.
# from sklearn.svm import LinearSVC, SVC
# from sklearn.neighbors import KNeighborsClassifier  # Classifier : 분류모델
# from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
# from sklearn.linear_model import LogisticRegression # 회귀가 아닌 분류 모델임

import warnings
warnings.filterwarnings('ignore')
import pandas as pd 

###########################################################

#1. DATA
dataset = load_diabetes()
x = dataset.data 
y = dataset.target 
# print(x.shape, y.shape)

# preprocessing >>  K-Fold 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=44)

# 전처리부분을 안써도 됨
# scaler = MinMaxScaler()
# scaler.fit(x_train)
# x_train = scaler.transform(x_train)
# x_test = scaler.transform(x_test)

#2. Modeling
# pipline : 파라미터튜닝에 전처리까지 합친다. >> 전처리와 모델을 합친다.

# # [1] Pipeline
parameters=[
    {'model__n_estimators' : [100, 200, 300], 'model__max_depth' : [6, 8, 10, 12]},
    {'model__max_depth' : [6, 8, 10, 12], 'model__min_samples_leaf' : [3, 7, 10]},
    {'model__min_samples_split' : [2, 3, 5, 9], 'model__n_jobs' : [-1, 2, 4]}
]

# # [2] make_pipeline
# parameters=[
#     {'randomforestregressor__n_estimators' : [100, 200], 'randomforestregressor__max_depth' : [6, 8, 10, 12]},
#     {'randomforestregressor__max_depth' : [6, 8, 10, 12], 'randomforestregressor__min_samples_leaf' : [3, 7, 10]},
#     {'randomforestregressor__min_samples_split' : [2, 3, 5, 9], 'randomforestregressor__n_jobs' : [-1, 2, 4]}
# ]

scaler = [MinMaxScaler(), StandardScaler()]
search = [RandomizedSearchCV, GridSearchCV]

for scale in scaler :
    pipe = Pipeline([("scaler", scale), ('model', RandomForestRegressor())])
    # pipe = make_pipeline(scale, RandomForestRegressor())

    for CV in search :
        model = CV(pipe, parameters, cv=5)
        model.fit(x_train, y_train)
        results = model.score(x_test, y_test)
        print(str(scale),str(CV)+':'+str(results))





# GridSearch
# 최적의 매개변수 :  RandomForestRegressor(max_depth=12, min_samples_leaf=10)
# 최종정답률 0.4838812611290275
# aaa  0.4838812611290275

# RandomSearch
# 최적의 매개변수 :  RandomForestRegressor(min_samples_leaf=10, min_samples_split=10)
# 최종정답률 0.47678641072030825
# aaa  0.47678641072030825

# pipeline (MinMaxscaler)
# model.score :  0.42556136196707384

# pipeline(Standardscaler)
# model.score:  0.41152922668231506

# pipeline
# MinMaxScaler() <class 'sklearn.model_selection._search.RandomizedSearchCV'>:0.48080011996690997
# MinMaxScaler() <class 'sklearn.model_selection._search.GridSearchCV'>:0.46004691837434464
# StandardScaler() <class 'sklearn.model_selection._search.RandomizedSearchCV'>:0.4760492602051315
# StandardScaler() <class 'sklearn.model_selection._search.GridSearchCV'>:0.47452782842686003