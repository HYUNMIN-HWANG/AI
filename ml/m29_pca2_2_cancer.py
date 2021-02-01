# PCA : 차원축소, 컬럼 재구성
# cumsum : 배열에서 주어진 축에 따라 누적되는 원소들의 누적 합을 계산하는 함수.

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA

datasets = load_breast_cancer()
x = datasets.data
y = datasets.target
print(x.shape, y.shape) # (569, 30) (569,)

# pca = PCA(n_components=9)
# x2 = pca.fit_transform(x)  # fit_transform : 전처리 fit과 transform 한꺼번에 한다.

# print(x2)
# print(x2.shape)            # (442, 7) >> 컬럼을 압축시켰다. 컬럼 재구성됨

# pca_EVR = pca.explained_variance_ratio_ # 컬럼이 어느 정도의 변화율을 보여주었는지 보여준다.
# print(pca_EVR)
# print(sum(pca_EVR)) 

pca = PCA()
pca.fit(x)
cumsum = np.cumsum(pca.explained_variance_ratio_)   
print("cumsum : ", cumsum)  # cumsum 누적 합을 계산
# cumsum :  [0.98204467 0.99822116 0.99977867 0.9998996  0.99998788 0.99999453
#  0.99999854 0.99999936 0.99999971 0.99999989 0.99999996 0.99999998
#  0.99999999 0.99999999 1.         1.         1.         1.
#  1.         1.         1.         1.         1.         1.
#  1.         1.         1.         1.         1.         1.        ]

d = np.argmax(cumsum >= 0.99)+1
print("cumsum >= 0.95", cumsum > 0.99)
print("d : ", d)
# cumsum >= 0.95 [False  True  True  True  True  True  True  True  True  True  True  True
#   True  True  True  True  True  True  True  True  True  True  True  True
#   True  True  True  True  True  True]
# d :  2

import matplotlib.pyplot as plt
plt.plot(cumsum)
plt.grid()
plt.show()


