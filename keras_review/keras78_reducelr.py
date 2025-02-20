# weight 값 조절

x_train = 0.5
y_train = 1.0   # 원래 y 값

########## 이부분 변경해보기 ##########
weight = 1.0
lr = 0.05
epoch = 100
########## 이부분 변경해보기 ##########

for iteration in range(epoch) :
    y_predict = x_train * weight
    error = (y_predict - y_train) ** 2

    print("Error : " + str(error) + "\ty_predict : " + str(y_predict))

    up_y_predict = x_train * (weight + lr)
    up_error = (y_train - up_y_predict) ** 2

    down_y_predict = x_train * (weight - lr)
    down_error = (y_train - down_y_predict) ** 2

    if (down_error <= up_error) :
        weight = weight - lr
    else :
        weight = weight + lr