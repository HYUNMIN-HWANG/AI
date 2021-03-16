import pandas as pd
import numpy as np

#1. DATA
wine = pd.read_csv('../data/csv/winequality-white.csv', header=0, sep=';',index_col=None)
# print(wine.head())

print(np.unique(wine['quality']))   # [3 4 5 6 7 8 9]

# 각 'quality' 수치 별 개수
count_data = wine.groupby('quality')['quality'].count()
print(count_data)
'''
quality
3      20
4     163
5    1457
6    2198
7     880
8     175
9       5
'''

# 'quality' 를 기준으로 각 컬럼마다 평균 구하기
mean_data = wine.groupby('quality').mean()
print(mean_data)
'''         fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  free sulfur dioxide  total sulfur dioxide   density        pH  sulphates    alcohol
quality
3             7.600000          0.333250     0.336000        6.392500   0.054300            53.325000            170.600000  0.994884  3.187500   0.474500  10.345000
4             7.129448          0.381227     0.304233        4.628221   0.050098            23.358896            125.279141  0.994277  3.182883   0.476135  10.152454
5             6.933974          0.302011     0.337653        7.334969   0.051546            36.432052            150.904598  0.995263  3.168833   0.482203   9.808840
6             6.837671          0.260564     0.338025        6.441606   0.045217            35.650591            137.047316  0.993961  3.188599   0.491106  10.575372
7             6.734716          0.262767     0.325625        5.186477   0.038191            34.125568            125.114773  0.992452  3.213898   0.503102  11.367936
8             6.657143          0.277400     0.326514        5.671429   0.038314            36.720000            126.165714  0.992236  3.218686   0.486229  11.636000
9             7.420000          0.298000     0.386000        4.120000   0.027400            33.400000            116.000000  0.991460  3.308000   0.466000  12.180000
'''

# quality == 9 인 데이터만 확인해보자
q9 = wine.groupby('quality').get_group(9)
print(q9)
'''
      fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  free sulfur dioxide  total sulfur dioxide  density    pH  sulphates  alcohol  quality
774             9.1              0.27         0.45            10.6      0.035                 28.0                 124.0  0.99700  3.20       0.46     10.4        9
820             6.6              0.36         0.29             1.6      0.021                 24.0                  85.0  0.98965  3.41       0.61     12.4        9
827             7.4              0.24         0.36             2.0      0.031                 27.0                 139.0  0.99055  3.28       0.48     12.5        9
876             6.9              0.36         0.34             4.2      0.018                 57.0                 119.0  0.98980  3.28       0.36     12.7        9
1605            7.1              0.26         0.49             2.2      0.032                 31.0                 113.0  0.99030  3.37       0.42     12.9        9
'''

# 각 그룹의 사이즈 확인하기
size = wine.groupby('quality').size()
print(size)
'''
quality
3      20
4     163
5    1457
6    2198
7     880
8     175
9       5
dtype: int64
'''

# quality 별 평균 확인
np_mean = wine.groupby('quality').agg(np.mean)
print(np_mean)
'''
         fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  free sulfur dioxide  total sulfur dioxide   density        pH  sulphates    alcohol
quality
3             7.600000          0.333250     0.336000        6.392500   0.054300            53.325000            170.600000  0.994884  3.187500   0.474500  10.345000
4             7.129448          0.381227     0.304233        4.628221   0.050098            23.358896            125.279141  0.994277  3.182883   0.476135  10.152454
5             6.933974          0.302011     0.337653        7.334969   0.051546            36.432052            150.904598  0.995263  3.168833   0.482203   9.808840
6             6.837671          0.260564     0.338025        6.441606   0.045217            35.650591            137.047316  0.993961  3.188599   0.491106  10.575372
7             6.734716          0.262767     0.325625        5.186477   0.038191            34.125568            125.114773  0.992452  3.213898   0.503102  11.367936
8             6.657143          0.277400     0.326514        5.671429   0.038314            36.720000            126.165714  0.992236  3.218686   0.486229  11.636000
9             7.420000          0.298000     0.386000        4.120000   0.027400            33.400000            116.000000  0.991460  3.308000   0.466000  12.180000
'''

# 최소
min = wine.groupby(by=['quality'], as_index=False).min()
print(min)
'''   quality  fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  free sulfur dioxide  total sulfur dioxide  density    pH  sulphates  alcohol
0        3            4.2              0.17         0.21             0.7      0.022                  5.0                  19.0  0.99110  2.87       0.28      8.0
1        4            4.8              0.11         0.00             0.7      0.013                  3.0                  10.0  0.98920  2.83       0.25      8.4
2        5            4.5              0.10         0.00             0.6      0.009                  2.0                   9.0  0.98722  2.79       0.27      8.0
3        6            3.8              0.08         0.00             0.7      0.015                  3.0                  18.0  0.98758  2.72       0.23      8.5
4        7            4.2              0.08         0.01             0.9      0.012                  5.0                  34.0  0.98711  2.84       0.22      8.6
5        8            3.9              0.12         0.04             0.8      0.014                  6.0                  59.0  0.98713  2.94       0.25      8.5
6        9            6.6              0.24         0.29             1.6      0.018                 24.0                  85.0  0.98965  3.20       0.36     10.4
'''

# 최대
max = wine.groupby(by=['quality'], as_index=False).max()
print(max)
'''
   quality  fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  free sulfur dioxide  total sulfur dioxide  density    pH  sulphates  alcohol
0        3           11.8             0.640         0.47           16.20      0.244                289.0                 440.0  1.00010  3.55       0.74     12.6
1        4           10.2             1.100         0.88           17.55      0.290                138.5                 272.0  1.00040  3.72       0.87     13.5
2        5           10.3             0.905         1.00           23.50      0.346                131.0                 344.0  1.00241  3.79       0.88     13.6
3        6           14.2             0.965         1.66           65.80      0.255                112.0                 294.0  1.03898  3.81       1.06     14.0
4        7            9.2             0.760         0.74           19.25      0.135                108.0                 229.0  1.00040  3.82       1.08     14.2
5        8            8.2             0.660         0.74           14.80      0.121                105.0                 212.5  1.00060  3.59       0.95     14.0
6        9            9.1             0.360         0.49           10.60      0.035                 57.0                 139.0  0.99700  3.41       0.61     12.9
'''

# SUM
sum = wine.groupby(by=['quality'], as_index=False).sum()
print(sum)
'''   quality  fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  free sulfur dioxide  total sulfur dioxide      density       pH  sulphates       alcohol
0        3         152.00             6.665         6.72          127.85      1.086               1066.5                3412.0    19.897680    63.75       9.49    206.900000
1        4        1162.10            62.140        49.59          754.40      8.166               3807.5               20420.5   162.067100   518.81      77.61   1654.850000
2        5       10102.80           440.030       491.96        10687.05     75.103              53081.5              219868.0  1450.097565  4616.99     702.57  14291.480000
3        6       15029.20           572.720       742.98        14158.65     99.388              78360.0              301230.0  2184.727045  7008.54    1079.45  23244.666667
4        7        5926.55           231.235       286.55         4564.10     33.608              30030.5              110101.0   873.358110  2828.23     442.73  10003.783333
5        8        1165.00            48.545        57.14          992.50      6.705               6426.0               22079.0   173.641290   563.27      85.09   2036.300000
6        9          37.10             1.490         1.93           20.60      0.137                167.0                 580.0     4.957300    16.54       2.33     60.900000
'''