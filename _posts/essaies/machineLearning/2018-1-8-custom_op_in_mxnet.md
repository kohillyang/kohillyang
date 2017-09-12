---
layout: post
title: Custom operator in mxnet
date: 2018-1-8 19:40
comments: true
external-url:
categories: machine-learning
permalink: /mxnet
---
<br>

```python
import mxnet as mx
import numpy as np

class TestReshape(mx.operator.CustomOp):
    def __init__(self, *args, **kwargs):
        pass
    def forward(self,is_train,req,in_data,out_data,aux):
        shape_in = in_data[0].shape
        shape_out = out_data[0].shape
        print(shape_in,shape_out)
        r = mx.nd.empty(shape = shape_out)
        for n_batch in range(shape_in[0]):
            for i in range(shape_in[2]):
                for j in range(shape_in[3]):
                    ch_expand = in_data[0][n_batch,:,i,j]
                    s_sqrt = int(np.sqrt(ch_expand.size))
                    ch_expand = ch_expand.reshape((s_sqrt,s_sqrt))
                    print(ch_expand.shape)
                    r[n_batch,0,i*ch_expand.shape[0]:(i+1)*ch_expand.shape[0],
                        j*(ch_expand.shape[0]):(j+1)*ch_expand.shape[1]] = ch_expand
        self.assign(out_data[0], req[0], r)
    def backward(self, req, out_grad, in_data, out_data, in_grad, aux):
        self.assign(in_grad[0], req[0],out_grad[0])
@mx.operator.register("testreshape")
class TestReshapeProp(mx.operator.CustomOpProp):
    def __init__(self):
        super(TestReshapeProp, self).__init__(need_top_grad=True)          
    def list_arguments(self):
        return ['data']
    def list_outputs(self):
        return ['output']
    def infer_shape(self, in_shape):
        data_shape = in_shape[0]
        output_shape = [data_shape[0],data_shape[1]//4,data_shape[2]*2,data_shape[3]*2]
        print(output_shape)
        return [data_shape], [output_shape], []
    def infer_type(self, in_type):
        dtype = in_type[0]
        return [dtype], [dtype], []
    def create_operator(self, ctx, shapes, dtypes):
        return TestReshape()
data_ = np.ones(shape = (2,4,3,3)).astype(np.float32)
data = mx.sym.Variable(name = "data",shape = (2,4,3,3))
sym = mx.symbol.Custom(data=data, name='softmax', op_type='testreshape')
sym = mx.symbol.identity(sym)
# mx.visualization.plot_network(sym,shape = {}).view()

model = sym.bind(ctx = mx.cpu(), args={'data':mx.nd.array(data_)},grad_req='null')

model.forward()
result = model.outputs[0].asnumpy()
print(result.shape)
print(np.sum(result,axis=1))





# td = np.empty(shape = (1,4,3,3),dtype = np.chararray)
# for m in range(td.shape[1]):
#     for n in range(td.shape[2]):
#         for p in range(td.shape[3]):
#             s = "{0}_{1}_{2}".format(m,n,p)
#             td[0,m,n,p] = s 
            # print(s)
# td = td.reshape((1,2,6,3))
# td = td.reshape((6,6))
# print(td)


# data = mx.sym.Variable(name = "data")
# label = mx.sym.Variable(name = "label")
# softmax = mx.sym.SoftmaxOutput(data=data, label=label, multi_output=True,
#                                     normalization='valid', use_ignore=True, ignore_label=-1, name="rpn_cls_prob",
#                                     grad_scale=1.0)

# data_ = np.array([[[[1,2,3],[1,2,3]],[[2,4,6],[1,2,3]]]])
# label_ = data_.copy()/1000
# print(data_.shape,label_.shape)                                    
# model = softmax.bind(ctx = mx.cpu(), args={'data':mx.nd.array(data_), 'label': mx.nd.array(label_)},grad_req='null')

# model.forward()
# result = model.outputs[0].asnumpy()
# print(result.shape)
# print(np.sum(result,axis=1))
```