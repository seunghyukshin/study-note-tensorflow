import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
import random

'''
Performance encreasing
1. Xavier initializing
2. Dropout
3. Adam optimizer
'''

mnist = input_data.read_data_sets("~/MINST_data", one_hot=True)

nb_classes = 10
keep_prob = tf.placeholder(tf.float32)

X = tf.placeholder(tf.float32, [None, 784])  # 784 = 28 * 28
Y = tf.placeholder(tf.float32, [None, nb_classes])  # 10: 0~9
W1 = tf.get_variable("W1", shape=[784, 512],
                     initializer=tf.contrib.layers.xavier_initializer())  # xavier로 초기화:초기값을 작게 잡아줌(성능 업)
b1 = tf.Variable(tf.random_normal([512]))
L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

W2 = tf.get_variable("W2", shape=[512, 512],
                     initializer=tf.contrib.layers.xavier_initializer())
b2 = tf.Variable(tf.random_normal([512]))
L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

W3 = tf.get_variable("W3", shape=[512, 512],
                     initializer=tf.contrib.layers.xavier_initializer())
b3 = tf.Variable(tf.random_normal([512]))
L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)
L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

W4 = tf.get_variable("W4", shape=[512, 512],
                     initializer=tf.contrib.layers.xavier_initializer())
b4 = tf.Variable(tf.random_normal([512]))
L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

W5 = tf.get_variable("W5", shape=[512, 512],
                     initializer=tf.contrib.layers.xavier_initializer())
b5 = tf.Variable(tf.random_normal([512]))
L5 = tf.nn.relu(tf.matmul(L4, W5) + b5)
L5 = tf.nn.dropout(L5, keep_prob=keep_prob)

W6 = tf.get_variable("W6", shape=[512, nb_classes],
                     initializer=tf.contrib.layers.xavier_initializer())
b6 = tf.Variable(tf.random_normal([nb_classes]))
hypothesis = tf.matmul(L5, W6) + b6

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

is_correct = tf.equal(tf.arg_max(hypothesis, 1), tf.arg_max(Y, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

# Train
training_epochs = 15
batch_size = 100
# if 1000 training examples, 1 epoch = batch size(500) * 2 iterations

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples / batch_size)

        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            c, _ = sess.run([cost, optimizer], feed_dict={X: batch_xs, Y: batch_ys, keep_prob: 0.7})
            avg_cost += c / total_batch  # 각 batch마다 가설을 세우고 cost를 구한 다음 모든 batch의 cost 평균
        print('Epoch:', '%04d' % (epoch + 1), 'cost = ', '{:.9f}'.format(avg_cost))

    # Test
    print("Accuracy: ", accuracy.eval(session=sess,
                                      feed_dict={X: mnist.test.images, Y: mnist.test.labels, keep_prob: 1}))

    ## Sample image show and prediction
    r = random.randint(0, mnist.test.num_examples - 1)
    print("Label: ", sess.run(tf.argmax(mnist.test.labels[r:r + 1], 1)))
    print("Prediction: ", sess.run(tf.argmax(hypothesis, 1),
                                   feed_dict={X: mnist.test.images[r:r + 1], keep_prob: 1}))

    plt.imshow(mnist.test.images[r:r + 1].reshape(28, 28), cmap='Greys',
               interpolation='nearest')  # 인덱스 r의 값을 리스트형태로 extract
    plt.show()
