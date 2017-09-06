---
layout: post
title: object detection-car
date: '2017-9-4 19:40'
comments: true
external-url: null
categories: machine-learning
---
<br>

所用的框架是mxnet，mxnet支持各种语言，比如ruby,python之类，中间也有一些坑：
<p>ImageDetIter继承自，ImageIter，ImageIter的定义在<code>/usr/local/lib/python3.5/dist-packages/mxnet/image/image.py</code>中能找到，这个类会自动对图像做一些预处理，比如自动resize，自动减去平均值，自动根据方差归一化之类的，*值得注意的是，似乎方差和均值并不是根据输入的图像自动计算出来的，而是作为参数输入或者使用一个定值（传说中的magic number?）*。</p>
<p>一个典型的ImageDetIter的写法如下：</p>

```python
train_iter = image.ImageDetIter(
    batch_size=batch_size,
    data_shape=(3, data_shape, data_shape),
    path_imgrec='./car_data/img_labeled.rec',
    path_imgidx='./car_data/img_labeled.idx',
    shuffle=True,
    mean=True,
    rand_crop=1,
    min_object_covered=0.95,
    max_attempts=200)
```
<p>ImageDetIter并不会用到全部的参数，多余的参数会以字典方式传入到`CreateDetAugmenter`中哦，而`CreateDetAugmenter`的部分源代码如下：</p>

```python
if mean is True:
    mean = np.array([123.68, 116.28, 103.53])
elif mean is not None:
    assert isinstance(mean, np.ndarray) and mean.shape[0] in [1, 3]

if std is True:
    std = np.array([58.395, 57.12, 57.375])
elif std is not None:
    assert isinstance(std, np.ndarray) and std.shape[0] in [1, 3]
```
<p>总之*方差和均值是可以通过mean和std传入的，想想居然有点小激动呢。*</p>
<p>另外一个小地方要注意的是，`img_labeled.idx`和`img_labeled.rec`是用官方的img2rec.py制作的，在制作过程中会用到一个lst文件，对于普通的图像分类算法，这个文件是可以通过img2rec.py本身生成，对于对象检测等涉及到多标签的问题，lst需要自己生成，生成的例子如下：</p>
<code>
```python
import cv2,os,sys
if len(sys.argv) > 1:
    rootPath = sys.argv[1]
else:
    rootPath = "./car_data/labeled/"
img_paths = []
for x,y,z in os.walk(rootPath):
    for name in z:
        path = os.path.join(x,name)    
        if path[-4:] in [".png",".jpg"]:
            img_paths.append(path)
for index,filePath in  enumerate(img_paths) :
    with open(filePath[:-4] + ".label","rt") as f:
        img = cv2.imread(filePath)
        xmin,ymin,xmax,ymax = map(lambda x:float(x),f.read().strip().split(" "))
        if xmin > xmax:
            tmp = [xmin,ymin]
            xmin,ymin = [xmax,ymax]
            xmax,ymax = tmp
        xmin /= img.shape[1]
        xmax /= img.shape[1]
        ymin /= img.shape[0]
        ymax /= img.shape[0]
        with open("car_data/img_labeled.lst","at") as f1:
#             f1.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n".format(
#                 index,2,5,img.shape[0],img.shape[1],index + 1,
#                 xmin,ymin,xmax,ymax,filePath[19:]))
            try:
                assert xmax > xmin
                assert ymax > ymin
                f1.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
                    index,
                    2,5,0,xmin,ymin,xmax,ymax,
                    filePath[19:]))
            except AssertionError:
                print(xmin*img.shape[1],xmax*img.shape[1])
                print(ymin*img.shape[0],ymax*img.shape[0])            
```

<p>之后调用img2re.py就行啦：</p>

```bash
LST_FILE_PREFIX:=./car_data/img_labeled
IMGS_DIR=./car_data/labeled/
IMG2REC=./incubator-mxnet-master/tools/im2rec.py
dataset:
  python3 $(IMG2REC) $(LST_FILE_PREFIX) $(IMGS_DIR) --pack-label=True
```
</code>

<p>*注意要加上--pack-label=True这个参数，反正注意就行了*<p>
