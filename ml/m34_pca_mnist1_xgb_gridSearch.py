# m31로 만든 0.95 이상의 n_componet를 사용하여 xgboost 모델을 만들 것 (mnist dnn 보다 성능 좋을 것)
# cnn과 비교한다.
# girdSearch & RandomSearchCV 

import numpy as np
from tensorflow.keras.datasets import mnist
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

#1. DATA
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x = np.append(x_train, x_test, axis=0)
x =x.reshape(70000, 28*28)  # 3차원은 PCA에 들어가지 않으므로 2차원으로 바꿔준다.
print(x.shape)  # (70000, 784)

y = np.append(y_train, y_test, axis=0)
print(y.shape)  # (70000,)

# pca = PCA() 
# pca.fit(x)
# cumsum = np.cumsum(pca.explained_variance_ratio_)
# print("cumsum : ", cumsum)

# d = np.argmax(cumsum >= 0.95)+1
# print("cumsum >= 0.95", cumsum > 0.95)
# print("d : ", d)    # d :  154

# import matplotlib.pyplot as plt
# plt.plot(cumsum)
# plt.grid()
# plt.show()

pca = PCA(n_components=154)
x2 = pca.fit_transform(x)

print(x2.shape)     # (70000, 154)

x_train, x_test, y_train, y_test = train_test_split(x2, y, train_size=0.8, shuffle=True, random_state=47)
print(x_train.shape)    # (56000, 154)
print(x_test.shape)     # (14000, 154)
print(y_train.shape, y_test.shape)  # (56000,) (14000,)
kf = KFold(n_splits=5, shuffle=True, random_state=47)

# from tensorflow.keras.utils import to_categorical
# y_train = to_categorical(y_train)
# y_test = to_categorical(y_test)
# print(y_train.shape)    # (56000, 10)
# print(y_test.shape)     # (14000, 10)

#2. Modling
parameters = [
    {"n_estimators":[90, 100], "learning_rate":[0.3, 0.001]},
    {"n_estimators":[90, 100], "learning_rate":[0.01, 0.001], "max_depth":[4, 5, 6]},
    {"colsample_bytree":[0.6, 0.9], "colsample_bylevel" :[0.6, 0.7, 0.9]}
]
model = GridSearchCV(XGBClassifier(n_jobs = 8, use_label_encoder=False, n_estimators=100), parameters, cv=kf)
                                    # n_estimators : epoch과 같은 개념, 몇 번 돌아가는 가

#3 Train
model.fit(x_train, y_train, eval_metric='mlogloss', verbose=True,
    eval_set=[(x_train, y_train), (x_test, y_test)]
    )
# eval_metrics : loss와 evaluate 합쳐져 있음
# eval_set : evaluate

#4 Evaluate, Predict
print("최적의 매개변수 : ", model.best_estimator_)

y_pred = model.predict(x_test) 

result = model.score(x_test, y_test)
print("result : ", result)

score = accuracy_score(y_pred, y_test)
print("accuracy_score : ", score)


# CNN
# loss :  0.034563612192869186
# acc :  0.9889000058174133
# y_test[:10] : [7 2 1 0 4 1 4 9 5 9]
# y_pred[:10] : [7 2 1 0 4 1 4 9 5 9]

# DNN
# loss :  0.10550455003976822
# acc :  0.9828000068664551
# y_test[:10] : [7 2 1 0 4 1 4 9 5 9]
# y_pred[:10] : [7 2 1 0 4 1 4 9 5 9]

# PCA(>0.95) - DNN
# loss :  0.09774444252252579
# acc :  0.9767143130302429
# y_test[:10] : [3 1 8 1 6 3 5 4 8 3]
# y_pred[:10] : [3 1 8 1 6 3 5 4 8 3]

# PCA(>1.0) - DNN
# loss :  0.14994649589061737
# acc :  0.9728571176528931
# y_test[:10] : [3 1 8 1 6 3 5 4 8 3]
# y_pred[:10] : [3 1 6 1 6 3 5 4 8 3]

# PCA(>0.95) - XGBoost
# result :  0.9644285714285714
# acc score :  0.9644285714285714

# PCA(>1.0) - XGBoost
# result :  0.9619285714285715

# PCA(>0.95) - XGBoost - gridSearch
# 최적의 매개변수 :  XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=0.7,
#               colsample_bynode=1, colsample_bytree=0.6, gamma=0, gpu_id=-1,
#               importance_type='gain', interaction_constraints='',
#               learning_rate=0.300000012, max_delta_step=0, max_depth=6,
#               min_child_weight=1, missing=nan, monotone_constraints='()',
#               n_estimators=200, n_jobs=8, num_parallel_tree=1,
#               objective='multi:softprob', random_state=0, reg_alpha=0,
#               reg_lambda=1, scale_pos_weight=None, subsample=1,
#               tree_method='exact', use_label_encoder=False,
#               validate_parameters=1, verbosity=None)
# result :  0.9686428571428571
# accuracy_score :  0.9686428571428571
