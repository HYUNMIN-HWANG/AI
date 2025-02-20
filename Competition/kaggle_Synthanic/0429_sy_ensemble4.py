# https://www.kaggle.com/remekkinas/ensemble-learning-meta-classifier-for-stacking/output 
import pandas as pd
import numpy as np
import random
import os

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold

import lightgbm as lgb
import catboost as ctb
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_graphviz

import graphviz
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter('ignore')
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier

TARGET = 'Survived'

N_ESTIMATORS = 1000
N_SPLITS = 10
SEED = 2021
EARLY_STOPPING_ROUNDS = 100
VERBOSE = 100

def set_seed(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    
set_seed(SEED)

# 데이터 불러오기
train_df = pd.read_csv('E:\data\kaggle_tabular/train.csv')
test_df = pd.read_csv('E:\data\kaggle_tabular/test.csv')
submission = pd.read_csv('E:\data\kaggle_tabular/sample_submission.csv')
test_df[TARGET] = pd.read_csv('E:\data\kaggle_tabular/pseudo_label.csv')[TARGET]

print(train_df.shape, test_df.shape, submission.shape)  # (100000, 12) (100000, 12) (100000, 2)

all_df = pd.concat([train_df, test_df]).reset_index(drop=True)

print(all_df.shape) # (200000, 12)

# 데이터 전처리
# Age fillna with mean age for each class
all_df['Age'] = all_df['Age'].fillna(all_df['Age'].mean())

# Cabin, fillna with 'X' and take first letter
all_df['Cabin'] = all_df['Cabin'].fillna('X').map(lambda x: x[0].strip())

# Ticket, fillna with 'X', split string and take first split 
all_df['Ticket'] = all_df['Ticket'].fillna('X').map(lambda x:str(x).split()[0] if len(str(x).split()) > 1 else 'X')

# Fare, fillna with mean value
fare_map = all_df[['Fare', 'Pclass']].dropna().groupby('Pclass').median().to_dict()
all_df['Fare'] = all_df['Fare'].fillna(all_df['Pclass'].map(fare_map['Fare']))
all_df['Fare'] = np.log1p(all_df['Fare'])

# Embarked, fillna with 'X' value
all_df['Embarked'] = all_df['Embarked'].fillna('X')

# Name, take only surnames
all_df['Name'] = all_df['Name'].map(lambda x: x.split(',')[0])

label_cols = ['Name', 'Ticket', 'Sex']
onehot_cols = ['Cabin', 'Embarked']
numerical_cols = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']

def label_encoder(c):
    le = LabelEncoder()
    return le.fit_transform(c)

scaler = StandardScaler()

onehot_encoded_df = pd.get_dummies(all_df[onehot_cols])
label_encoded_df = all_df[label_cols].apply(label_encoder)
numerical_df = pd.DataFrame(scaler.fit_transform(all_df[numerical_cols]), columns=numerical_cols)
target_df = all_df[TARGET]

all_df = pd.concat([numerical_df, label_encoded_df, onehot_encoded_df, target_df], axis=1)
print(all_df.head())
print(all_df.shape) # (200000, 22)

# 모델 앙상블
# [1] LGBMRegressor
print("LGBMRegressor>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
params = {
    #'metric': 'binary_logloss',
    'n_estimators': N_ESTIMATORS,
    'objective': 'binary',
    'random_state': SEED,
    'learning_rate': 0.01,
    'min_child_samples': 150,
    'reg_alpha': 3e-5,
    'reg_lambda': 9e-2,
    'num_leaves': 20,
    'max_depth': 16,
    'colsample_bytree': 0.8,
    'subsample': 0.8,
    'subsample_freq': 2,
    'max_bin': 240,
}

lgb_oof = np.zeros(train_df.shape[0])
lgb_preds = np.zeros(test_df.shape[0])
feature_importances = pd.DataFrame()

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

for fold, (train_idx, valid_idx) in enumerate(skf.split(all_df, all_df[TARGET])):
    print(f"===== FOLD {fold} =====")
    oof_idx = np.array([idx for idx in valid_idx if idx < train_df.shape[0]])
    preds_idx = np.array([idx for idx in valid_idx if idx >= train_df.shape[0]])
    print(train_idx.shape)  # (180000,)
    print(oof_idx.shape, preds_idx.shape) # (9986,) (10014,)

    X_train, y_train = all_df.iloc[train_idx].drop(TARGET, axis=1), all_df.iloc[train_idx][TARGET]
    X_valid, y_valid = all_df.iloc[oof_idx].drop(TARGET, axis=1), all_df.iloc[oof_idx][TARGET]
    X_test = all_df.iloc[preds_idx].drop(TARGET, axis=1)
    print(X_train.shape, y_train.shape) # (180000, 21) (180000,)
    print(X_valid.shape, y_valid.shape)   # (9986, 21) (9986,)
    print(X_test.shape) # (10014, 21)


    pre_model = lgb.LGBMRegressor(**params)
    pre_model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train),(X_valid, y_valid)],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        verbose=VERBOSE
    )

    params2 = params.copy()
    params2['learning_rate'] = params['learning_rate'] * 0.1
    model = lgb.LGBMRegressor(**params2)
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train),(X_valid, y_valid)],
        early_stopping_rounds=EARLY_STOPPING_ROUNDS,
        verbose=VERBOSE,
        init_model=pre_model
    )
    
    fi_tmp = pd.DataFrame()
    fi_tmp["feature"] = model.feature_name_
    fi_tmp["importance"] = model.feature_importances_
    fi_tmp["fold"] = fold
    fi_tmp["seed"] = SEED
    feature_importances = feature_importances.append(fi_tmp)
    
    lgb_oof[oof_idx] = model.predict(X_valid)
    lgb_preds[preds_idx-train_df.shape[0]] = model.predict(X_test)
    
    acc_score = accuracy_score(y_valid, np.where(lgb_oof[oof_idx]>0.5, 1, 0))
    print(f"===== ACCURACY SCORE {acc_score:.6f} =====\n")
    
  
acc_score = accuracy_score(all_df[:train_df.shape[0]][TARGET], np.where(lgb_oof>0.5, 1, 0))
print(f"===== ACCURACY SCORE {acc_score:.6f} =====")

# [2] CatBoostClassifier
print("CatBoostClassifier>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
params = {
    'bootstrap_type': 'Poisson',
    'loss_function': 'Logloss',
    'eval_metric': 'Logloss',
    'random_seed': SEED,
    'task_type': 'GPU',
    'max_depth': 8,
    'learning_rate': 0.01,
    'n_estimators': N_ESTIMATORS,
    'max_bin': 280,
    'min_data_in_leaf': 64,
    'l2_leaf_reg': 0.01,
    'subsample': 0.8
}

ctb_oof = np.zeros(train_df.shape[0])
ctb_preds = np.zeros(test_df.shape[0])
feature_importances = pd.DataFrame()

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

for fold, (train_idx, valid_idx) in enumerate(skf.split(all_df, all_df[TARGET])):
    print(f"===== FOLD {fold} =====")
    oof_idx = np.array([idx for idx in valid_idx if idx < train_df.shape[0]])
    preds_idx = np.array([idx for idx in valid_idx if idx >= train_df.shape[0]])

    X_train, y_train = all_df.iloc[train_idx].drop(TARGET, axis=1), all_df.iloc[train_idx][TARGET]
    X_valid, y_valid = all_df.iloc[oof_idx].drop(TARGET, axis=1), all_df.iloc[oof_idx][TARGET]
    X_test = all_df.iloc[preds_idx].drop(TARGET, axis=1)
    
    model = ctb.CatBoostClassifier(**params)
    model.fit(X_train, y_train,
              eval_set=[(X_valid, y_valid)],
              use_best_model=True,
              early_stopping_rounds=EARLY_STOPPING_ROUNDS,
              verbose=VERBOSE
              )
    
    fi_tmp = pd.DataFrame()
    fi_tmp["feature"] = X_test.columns.to_list()
    fi_tmp["importance"] = model.get_feature_importance()
    fi_tmp["fold"] = fold
    fi_tmp["seed"] = SEED
    feature_importances = feature_importances.append(fi_tmp)
    
    ctb_oof[oof_idx] = model.predict(X_valid)
    ctb_preds[preds_idx-train_df.shape[0]] = model.predict(X_test)
    
    acc_score = accuracy_score(y_valid, np.where(ctb_oof[oof_idx]>0.5, 1, 0))
    print(f"===== ACCURACY SCORE {acc_score:.6f} =====\n")
    
acc_score = accuracy_score(all_df[:train_df.shape[0]][TARGET], np.where(ctb_oof>0.5, 1, 0))
print(f"===== ACCURACY SCORE {acc_score:.6f} =====")

# [3] DecisionTreeClassifier
print(" DecisionTreeClassifier>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# Tuning the DecisionTreeClassifier by the GridSearchCV
parameters = {
    'max_depth': np.arange(2, 5, dtype=int),
    'min_samples_leaf':  np.arange(2, 5, dtype=int)
}

classifier = DecisionTreeClassifier(random_state=2021)

model = GridSearchCV(
    estimator=classifier,
    param_grid=parameters,
    scoring='accuracy',
    cv=10,
    n_jobs=-1)
model.fit(X_train, y_train)

best_parameters = model.best_params_
print(best_parameters)

dtm_oof = np.zeros(train_df.shape[0])
dtm_preds = np.zeros(test_df.shape[0])
feature_importances = pd.DataFrame()

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

for fold, (train_idx, valid_idx) in enumerate(skf.split(all_df, all_df[TARGET])):
    print(f"===== FOLD {fold} =====")
    oof_idx = np.array([idx for idx in valid_idx if idx < train_df.shape[0]])
    preds_idx = np.array([idx for idx in valid_idx if idx >= train_df.shape[0]])

    X_train, y_train = all_df.iloc[train_idx].drop(TARGET, axis=1), all_df.iloc[train_idx][TARGET]
    X_valid, y_valid = all_df.iloc[oof_idx].drop(TARGET, axis=1), all_df.iloc[oof_idx][TARGET]
    X_test = all_df.iloc[preds_idx].drop(TARGET, axis=1)
    
    model = DecisionTreeClassifier(
        max_depth=best_parameters['max_depth'],
        min_samples_leaf=best_parameters['min_samples_leaf'],
        random_state=SEED
    )
    model.fit(X_train, y_train)
    
    dtm_oof[oof_idx] = model.predict(X_valid)
    dtm_preds[preds_idx-train_df.shape[0]] = model.predict(X_test)
    
    acc_score = accuracy_score(y_valid, np.where(dtm_oof[oof_idx]>0.5, 1, 0))
    print(f"===== ACCURACY SCORE {acc_score:.6f} =====\n")
    
acc_score = accuracy_score(all_df[:train_df.shape[0]][TARGET], np.where(dtm_oof>0.5, 1, 0))
print(f"===== ACCURACY SCORE {acc_score:.6f} =====")

# [4] XGBoost Classifier
print(" XGBoost Classifier >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# Tuning the XGBoost Classifier by the GridSearchCV
parameters = {
    'max_depth': np.arange(2, 5, dtype=int),
    # 'min_samples_leaf':  np.arange(2, 5, dtype=int)
}

classifier = XGBClassifier(n_estimators=1000) 

model = GridSearchCV(
    estimator=classifier,
    param_grid=parameters,
    scoring='accuracy',
    cv=10,
    n_jobs=-1)
model.fit(X_train, y_train)

best_parameters = model.best_params_
print(best_parameters)

svc_oof = np.zeros(train_df.shape[0])
svc_preds = np.zeros(test_df.shape[0])
feature_importances = pd.DataFrame()

mod = ('XGBoost Classifier',XGBClassifier(random_state=SEED,
    cv=5,n_estimator=1000,verbosity=0, n_jobs=-1,learning_rate=.1, max_depth=best_parameters['max_depth']))

skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

for fold, (train_idx, valid_idx) in enumerate(skf.split(all_df, all_df[TARGET])):
    print(f"===== FOLD {fold} =====")
    oof_idx = np.array([idx for idx in valid_idx if idx < train_df.shape[0]])
    preds_idx = np.array([idx for idx in valid_idx if idx >= train_df.shape[0]])

    X_train, y_train = all_df.iloc[train_idx].drop(TARGET, axis=1), all_df.iloc[train_idx][TARGET]
    X_valid, y_valid = all_df.iloc[oof_idx].drop(TARGET, axis=1), all_df.iloc[oof_idx][TARGET]
    X_test = all_df.iloc[preds_idx].drop(TARGET, axis=1)
    
    model = mod[1]
    model.fit(X_train, y_train)
    
    svc_oof[oof_idx] = model.predict(X_valid)
    svc_preds[preds_idx-train_df.shape[0]] = model.predict(X_test)
    
    acc_score = accuracy_score(y_valid, np.where(svc_oof[oof_idx]>0.5, 1, 0))
    print(f"===== ACCURACY SCORE {acc_score:.6f} =====\n")
    
acc_score = accuracy_score(all_df[:train_df.shape[0]][TARGET], np.where(svc_oof>0.5, 1, 0))
print(f"===== ACCURACY SCORE {acc_score:.6f} =====")

# Submission
submission['submit_lgb'] = np.where(lgb_preds>0.5, 1, 0)
submission['submit_ctb'] = np.where(ctb_preds>0.5, 1, 0)
submission['submit_dtm'] = np.where(dtm_preds>0.5, 1, 0)
submission['submit_svc'] = np.where(svc_preds>0.5, 1, 0)

submission[[col for col in submission.columns if col.startswith('submit_')]].sum(axis = 1).value_counts()

submission[TARGET] = (submission[[col for col in submission.columns if col.startswith('submit_')]].sum(axis=1) >= 3).astype(int)
submission.drop([col for col in submission.columns if col.startswith('submit_')], axis=1, inplace=True)

submission['submit_1'] = submission[TARGET].copy()
submission['submit_2'] = pd.read_csv("E:\\data\\kaggle_tabular\\submission\\submission_0429_voting6.csv")[TARGET]
submission['submit_3'] = pd.read_csv("E:\\data\\kaggle_tabular\\pseudo_label.csv")[TARGET]

submission[[col for col in submission.columns if col.startswith('submit_')]].sum(axis = 1).value_counts()

submission[TARGET] = (submission[[col for col in submission.columns if col.startswith('submit_')]].sum(axis=1) >= 2).astype(int)

submission[['PassengerId', TARGET]].to_csv("E:\\data\\kaggle_tabular\\submission_0429_voting7.csv", index = False)

# submission_0429_voting7.csv -> hhm2816 학원컴
# score : 0.81726
