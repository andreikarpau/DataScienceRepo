import tensorflow as tf

conv_filt_shape = [3, 3, 1, 1]
weights = tf.Variable(tf.truncated_normal(conv_filt_shape, stddev=0.03), name="Bla" + '_W')
out_layer = tf.nn.relu(weights)

ksize = [1, 2, 2, 1]
strides = [1, 2, 2, 1]
max_pool = tf.nn.max_pool(out_layer, ksize=ksize, strides=strides, padding='SAME')

init_op = tf.global_variables_initializer()

with tf.Session() as sess:
    # initialise the variables
    sess.run(init_op)

    print(weights.eval())
    print("----------------------------------\n")
    print(out_layer.eval())
    print("----------------------------------\n")
    print(max_pool.eval())
    print("Test!!!")

