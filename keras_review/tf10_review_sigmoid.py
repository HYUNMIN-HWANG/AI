import tensorflow as tf

tf.set_random_seed(66)

x_data = [[1,2],[2,3],[3,1],
          [4,3],[5,3],[6,2]]
y_data = [[0],[0],[0],
          [1],[1],[1]]  # 0과 1로 이루어진 이진분류

x = tf.placeholder(tf.float32, shape=[None,2])
y = tf.placeholder(tf.float32, shape=[None,1])

w = tf.Variable(tf.random_normal([2,1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

# sigmoid
hypothesis = tf.sigmoid(tf.matmul(x , w) + b)
# binary_crossentropy
cost = -tf.reduce_mean(y*tf.log(hypothesis)+(1-y)*tf.log(1-hypothesis))

train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

predicted = tf.cast(hypothesis > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted,y),dtype=tf.float32))

with tf.Session() as sess :
    sess.run(tf.global_variables_initializer())

    for step in range (2001) :
        _, cost_val = sess.run([train, cost], feed_dict={x:x_data, y:y_data})

        if step % 20 == 0 :
            print(step, cost_val)
    
    h, c, a = sess.run([hypothesis, predicted, accuracy], feed_dict={x:x_data, y:y_data})
    print("hypothesis", h, "\npredicted", c, "\naccuracy",a)