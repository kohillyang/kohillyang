---
layout: post
title: Tensorflow
date: 2017-02-13 19:40
comments: true
external-url:
categories: machine-learning
permalink: /tensorflow
---
<br>
### 初始化成员变量
tensorflow中Variable变量是由Session管理的，对其进行初始化会让Session开始追踪这个Variable变量


### 常见层
* 卷积层

```bash
tf.nn.depthwise_conv2d，连接不同卷积层，例如用来构建Inception网络。
tf.nn.separable_conv2d，类似于tf.nn.conv2d，能够牺牲精度换取速度，在大型网络中十分有用。
tf.nn.conv2d_transpose，反卷积
```

* 激活函数

```bash
tf.nn.relu
tf.nn.sigmoid
tf.nn.tanh
tf.nn.dropout
```

* 池化

```bash
tf.nn.max_pool
tf.nn.avg_pool
```


* 归一化

`tf.nn.local_response_normalization`

* 其他

```bash
tf.contrib.layers.convolution2d
tf.contrib.layers.fully_connected
```

### Profile

如果使用Pytorch或者Gluon, 应该是可以设置成同步计算再用Python自带的Profile工具的。

对于Tensorflow，Tensorflow自己提供了Profile工具，大概如下：
```python
run_metadata = tf.RunMetadata()
dense_decoded = sess.run([g.dense_decoded], test_feed,
                            options=tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE),run_metadata=run_metadata
                            )
lastbatch_err, lr = sess.run([g.lerr, g.learning_rate], test_feed,
                            options=tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE),run_metadata=run_metadata
                        )
trace = timeline.Timeline(step_stats=run_metadata.step_stats)
trace_file = open('timeline.ctf.json', 'w')
trace_file.write(trace.generate_chrome_trace_format())
```

然后可以在chrome里输入`chrome://tracing/`，在里面加载上述代码保存的json文件，即可看到图形化的Profile结果。

