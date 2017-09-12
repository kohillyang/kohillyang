---
layout: post
title: model_conversion
date: 2018-1-14 15:07
comments: true
categories: machine-learning
author: kohill
---
<br>
### convert from mxnet to tensorflow
主要是使用微软出的mmdnn,测试版本是mmdnn 0.1.2，在mxnet 1.0上测试失败，因此推荐版本是mxnet 0.11.0，测试的网络为官方的resnet-18。

使用以下命令安装mmdnn，
```
pip install https://github.com/Microsoft/MMdnn/releases/download/0.1.2/mmdnn-0.1.2-py2.py3-none-any.whl
```

mxnet训练得到的模型有两个文件，其中params保存了网络的参数，json保存了网络的结构，使用以下命令将其转换为中间格式：
```
output_prefix=‘output/resnet_18’
python -m mmdnn.conversion._script.convertToIR -f mxnet -n ../../mx-text/models/resnet-18-release-symbol.json -w ../../mx-text/models/resnet-18-release-0000.params -d $(output_prefix) --inputShape 3  512 512
```

上面的命令会输出一个pb文件，保存了权重信息，以及一个json文件，保存了网络结构信息，之后使用下面的命令将其转为tensorlfow 格式

```
output_prefix=‘output/resnet_18’
python -m mmdnn.conversion._script.IRToCode -f tensorflow --IRModelPath $(output_prefix).pb --IRWeightPath $(output_prefix).npy --dstModelPath $(output_prefix).py
```

第一次使用时，上面的命令会报下面的错误

```
Traceback (most recent call last):
  File "/home/hszc/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/hszc/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/_script/IRToCode.py", line 120, in <module>
    _main()
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/_script/IRToCode.py", line 115, in _main
    ret = _convert(args)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/_script/IRToCode.py", line 56, in _convert
    emitter.run(args.dstModelPath, args.dstWeightPath, args.phase)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/common/DataStructure/emitter.py", line 21, in run
    self.save_code(dstNetworkPath, phase)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/common/DataStructure/emitter.py", line 53, in save_code
    code = self.gen_code(phase)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/tensorflow/tensorflow_emitter.py", line 81, in gen_code
    func(current_node)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/tensorflow/tensorflow_emitter.py", line 107, in emit_Conv
    input_node, padding = self._defuse_padding(IR_node)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/tensorflow/tensorflow_emitter.py", line 132, in _defuse_padding
    padding = convert_onnx_pad_to_tf(padding)
  File "/home/hszc/anaconda2/lib/python2.7/site-packages/mmdnn/conversion/common/utils.py", line 62, in convert_onnx_pad_to_tf
    return np.transpose(np.array(pads).reshape([2, -1])).reshape(-1, 2).tolist()
```


解决该问题的方法为，将函数`convert_onnx_pad_to_tf`（位置见报错信息）修改为，
```python
def convert_onnx_pad_to_tf(pads):
    print pads
    return np.transpose(np.array(pads).reshape([2, -1])).reshape(-1, 2).tolist() if pads is not None else 0
```

之后再执行上面的命令便可成功，成功之后可以得到包含模型权重的npy文件以及模型的py文件。

py文件其中一部分如下：

```python
import tensorflow as tf

__weights_dict = dict()

is_train = False

def load_weights(weight_file):
    import numpy as np

    if weight_file == None:
        return

    try:
        weights_dict = np.load(weight_file).item()
    except:
        weights_dict = np.load(weight_file, encoding='bytes').item()

    return weights_dict


def KitModel(weight_file = None):
    global __weights_dict
    __weights_dict = load_weights(weight_file)

    oass

def batch_normalization(input, name, **kwargs):
    mean = tf.Variable(__weights_dict[name]['mean'], name = name + "_mean", trainable = is_train)
    variance = tf.Variable(__weights_dict[name]['var'], name = name + "_var", trainable = is_train)
    offset = tf.Variable(__weights_dict[name]['bias'], name = name + "_bias", trainable = is_train) if 'bias' in __weights_dict[name] else None
    scale = tf.Variable(__weights_dict[name]['scale'], name = name + "_scale", trainable = is_train) if 'scale' in __weights_dict[name] else None
    return tf.nn.batch_normalization(input, mean, variance, offset, scale, name = name, **kwargs)


def convolution(input, name, group, **kwargs):
    w = tf.Variable(__weights_dict[name]['weights'], trainable=is_train, name=name + "_weight")
    if group == 1:
        layer = tf.nn.convolution(input, w, **kwargs)
    else:
        weight_groups = tf.split(w, num_or_size_splits=group, axis=-1)
        xs = tf.split(input, num_or_size_splits=group, axis=-1)
        convolved = [tf.nn.convolution(x, weight, **kwargs) for
                    (x, weight) in zip(xs, weight_groups)]
        layer = tf.concat(convolved, axis=-1)

    if 'bias' in __weights_dict[name]:
        b = tf.Variable(__weights_dict[name]['bias'], trainable=is_train, name=name + "_bias")
        layer = layer + b
    return layer

```

将其中的函数convolution做适当修改：

```python
def convolution(input, name, **kwargs):
    try:
        if kwargs['padding']=="":
            kwargs['padding']="SAME"
    except KeyError:
        pass

    try:
        if kwargs['paddings']=="":
            kwargs['paddings']="SAME"
    except KeyError:
        pass
    try:
        if kwargs['strides']==[]:
            kwargs['strides']=[1,1]
    except KeyError:
        pass    
    print(__weights_dict[name]['weights'].shape)
    w = tf.Variable(__weights_dict[name]['weights'], trainable = is_train, name = name + "_weight")
    layer = tf.nn.convolution(input, w, **kwargs)
    if 'bias' in __weights_dict[name]:
        b = tf.Variable(__weights_dict[name]['bias'], trainable = is_train, name = name + "_bias")
        layer = layer + b
    return layer
```

另外，代码中id是关键字，应该把它改成data，如下面的第二行
```python
    data            = tf.placeholder(tf.float32, shape = (None, 512, 512, 3), name = 'data')
    bn_data         = batch_normalization(id, variance_epsilon=1.99999994948e-05, name='bn_data')
    conv0_pad       = tf.pad(bn_data, paddings = [[0L, 0L], [3L, 3L], [3L, 3L], [0L, 0L]])
```

最终我们得到了模型的py文件和权重的npy文件，一个使用它们的方法如下：

```python
import resnet_18 as mx_sym
import tensorflow as tf
import cv2,os
import numpy as np
import matplotlib.pyplot as plt
threthold = 0.4
from random import  randint
randcolor = lambda : (randint(128,255),randint(128,255),randint(128,255))
sess = tf.Session()
net = mx_sym.KitModel("output/resnet_18.npy")
init = tf.global_variables_initializer()
sess.run(init)


saver = saver = tf.train.Saver(tf.all_variables())
saver.save(sess, "output/tf_model/model.ckpt", global_step=0)

output_graph = output_graph =   "frozen_model.pb"
# We use a built-in TF helper to export variables to constants
output_graph_def = tf.graph_util.convert_variables_to_constants(
    sess, # The session is used to retrieve the weights
    tf.get_default_graph().as_graph_def(), # The graph_def is used to retrieve the nodes
    ["add_last"], # The output node names are used to select the usefull nodes
)

# Finally we serialize and dump the output graph to the filesystem
with tf.gfile.GFile(output_graph, "wb") as f:
    f.write(output_graph_def.SerializeToString())
print("%d ops in the final graph." % len(output_graph_def.node))

```

如果你对mxnet 和tensorlfow 都比较熟悉，应该是能看懂上面的代码的。

完整过程的Makefile如下：
```python
#../../mx-text/models/resnet-18-release-0000.params ../../mx-text/models/resnet-18-release-symbol.json
input_prefix:=
output_prefix:=output/resnet_18
all:
	-mkdir -p output
	python -m mmdnn.conversion._script.convertToIR -f mxnet -n ../../mx-text/models/resnet-18-release-symbol.json -w ../../mx-text/models/resnet-18-release-0000.params -d $(output_prefix) --inputShape 3 512 512
	python -m mmdnn.conversion._script.IRToCode -f tensorflow --IRModelPath $(output_prefix).pb --IRWeightPath $(output_prefix).npy --dstModelPath $(output_prefix).py
#python -m mmdnn.conversion.examples.tensorflow.imagenet_test -n $(output_prefix) -w $(output_prefix).npy --dump $(output_prefix).ckpt
	python model_saver.py
#	python test_mxnet_converter.py
```
