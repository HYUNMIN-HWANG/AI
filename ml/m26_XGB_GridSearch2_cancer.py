# xgboost & gridsearch

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import datetime

import numpy as np
import pandas as pd

#1. DATA
dataset = load_breast_cancer()
x = dataset.data 
y = dataset.target

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=44)
kf = KFold(n_splits=5, shuffle=True, random_state=47)

#2. modeling
parameters = [
    {"n_estimators":[100, 200, 300], "learning_rate":[0.1, 0.3, 0.001, 0.01], "max_depth":[4, 5, 6]},
    {"n_estimators":[90, 100, 110], "learning_rate":[0.1, 0.01, 0.001], "max_depth":[4, 5, 6], "colsample_bytree":[0.6, 0.9, 1]},
    {"n_estimators":[90, 100], "learning_rate":[0.1, 0.05, 0.001], "max_depth":[4, 5, 6], "colsample_bytree":[0.6, 0.9, 1], "colsample_bylevel" :[0.6, 0.7, 0.9]}
]
model = GridSearchCV(XGBClassifier(n_jobs = -1, use_label_encoder=False), parameters, cv=kf)

#3. Train
model.fit(x_train, y_train, eval_metric='logloss')

#4. Score, Predict
result = model.score(x_test, y_test)
print("model.score : ", result)

y_pred = model.predict(x_test)

score = accuracy_score(y_pred, y_test)
print("accuracy_score : ", score)

# GridSearchCV
# result :  0.9649122807017544
# acc score :  0.9649122807017544