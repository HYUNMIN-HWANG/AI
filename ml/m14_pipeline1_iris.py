# Pipeline : 파라미터튜닝에 전처리까지 합친다. >> 전처리와 모델을 합친다.

import numpy as np
from sklearn.datasets import load_iris

from sklearn.preprocessing import MinMaxScaler, StandardScaler  # 둘 중에 하나 사용
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline, make_pipeline

# 모델마다 나오는 결과 값을 비교한다.
from sklearn.svm import LinearSVC, SVC
# from sklearn.neighbors import KNeighborsClassifier  # Classifier : 분류모델
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression # 회귀가 아닌 분류 모델임

import warnings
warnings.filterwarnings('ignore')
import pandas as pd 

###########################################################

#1. DATA
dataset = load_iris()
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
                # 전처리 scaler 이름설정        # model  이름설정  
# model = Pipeline([("scaler", MinMaxScaler()), ('malddong', SVC())])
# model = Pipeline([("scaler", StandardScaler()), ('malddong', SVC())])

# # [2] make_pipeline
# model = make_pipeline(MinMaxScaler(), SVC())
model = make_pipeline(StandardScaler(), SVC())

model.fit(x_train, y_train)

results = model.score(x_test, y_test)
print("model.score : ", results)   




# gridSearch
# 최적의 매개변수 :  RandomForestClassifier(max_depth=10, min_samples_leaf=7)
# 최종정답률 0.9333333333333333
# aaa  0.9333333333333333

# RandomSearch
# 최적의 매개변수 :  RandomForestClassifier(min_samples_split=9, n_jobs=-1)
# 최종정답률 0.9666666666666667
# aaa  0.9666666666666667

# pipeline (MinMaxscaler)
# model.score :  0.9666666666666667

# pipeline (StandardScaler)
# model.score :  0.9666666666666667