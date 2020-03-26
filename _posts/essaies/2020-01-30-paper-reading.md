---
layout: post
title: Paper Reading
date: 2019-7-13 19:40
comments: true 
external-url:
categories: linux
permalink: /paper_reading
---
<br>

### VOI 论文 

基于滤波的方法：

MSCKF（2007）, VIO很经典的一篇论文

ROVIO, 光度误差/重投影误差

Stereo-MSCKF 开源的MSCKF（2018）

基于优化的VIO：
OKVIS 最早基于优化的VIO系统（开源）
TRO， SVO+预积分，预积分公式非常细致，复现论文Learn-VIO-ORB
VINS-Mono


### 论文阅读 Is Levenberg-Marquardt the Most Efficient Optimization Algorithm for Implementing Bundle Adjustment? 

论文链接 <https://projects.ics.forth.gr/_publications/0201-P0401-lourakis-levenberg.pdf>


### 非线性最小二乘

对于一个最小二乘问题,注意$\mathbf{W}$为对称矩阵： 

$$\begin{aligned}
    \mathop{min} \mathbf{F}(x) &= \mathbf{f}^{T}(x)\mathbf{W}\mathbf{f}(x)\\
    \mathbf{f}(x+h) &\simeq \mathbf{f}(x) + \mathbf{J}\mathbf{h}\\
    F(x+h) &= \frac{1}{2}f(x+h)^{T}Wf(x+h) \simeq L(h) \\
    L(h) &= \frac{1}{2}(\mathbf{f}(x) + \mathbf{J}\mathbf{h}) ^ T W (\mathbf{f}(x) + \mathbf{J}\mathbf{h})\\     &= \frac{1}{2} \left[  f^T(x)Wf(x)  + 2h^TJ^TW(x)f(x) + h^TJ^TWJh  \right] \\
     &= \frac{1}{2} \left[  F(x)  + 2h^Tg + h^THh  \right] \\
     -L(0)+L(h) &= h^Tg + \frac{1}{2}h^THh \\
     -L(0)+L(h_{gn}) &= h_{gn}^Tg + \frac{1}{2}h_{gn}^THh_{gn} \\
                    &= \frac{1}{2} h_{gn}^Tg\end{aligned}$$

增益系数 

$$\begin{aligned}
    \rho &= \frac{F(x+h)-F(x)}{L(h)-L(0)}\\
        &= \frac{F(x+h)-F(x)}{h^Tg + \frac{1}{2}h^THh}\end{aligned}$$

$L(h)$对$h$的一阶导和二阶导为： 

$$\begin{aligned}
    L'(x) = g(x) &= \frac{dL(h)}{dh} = J^TWf(x)+ h^TJ^TWJ\\
    H(x) &= \frac{d^2L(h)}{dh^2} = J^TWJ\end{aligned}$$

令一阶导等于0，可以得到正规方程(normal equation)： 

$$J^TWJh = -J^TWf(x)$$

LM(Dampled Gauss-Newton method, Levenberg-Marquardt Method),正规方程变为： 

$$(J^TWJ + \lambda \mathbf{I})h_{lm} = -J^TWf(x)$$

当阻尼系数$\lambda$比较大的时候，上式趋近于梯度下降法，当$\lambda$趋近于0时，上式趋近于高斯牛顿法

参考论文：

```bash
1. The Levenberg-Marquardt method for nonlinear least squares curve-fitting problems
2. Is Levenberg-Marquardt the Most Efficient Optimization Algorithm for
Implementing Bundle Adjustment?
3. METHODS FOR NON-LINEAR LEAST SQUARES PROBLEMS.
其中1介绍了3中LM中的阻尼因子的更新方法，2对比了在SLAM问题中，Dogleg与LM的精度，结果Dogleg稍好于LM，3详细介绍了Dogleg与LM算法。
```

### 3D地表重建主流框架
`1`. Colmap(开源， 需要cuda)<br>
`2`. OpenDroneMap（开源）<br>
`3`. Altizure(OpenDroneMap（开源）)

Steps of 3D reconstruction by ODM(from <https://community.opendronemap.org/t/where-can-i-find-background-information-on-the-concepts-of-odm/665/2>).

```
In short, the steps are:

    1. Images metadata extraction (GPS location, coordinate system)
    2. Structure from motion (from images to camera positions/orientations and sparse point cloud). We use OpenSfM for this.
    3. Multi view stereo (from camera + images to dense point clouds)
    4. Meshing (from points clouds to triangle meshes, we use mostly a Poisson Reconstruction approach but have support for 2.5D meshing as well)
    5. Texturing (from camera + images + meshes to textured meshes)
    6. Georeferencing (from local coordinates + GPS and/or ground control points to real world coordinates)
    7. DSM/DTM (from real world points to elevation models)
    8. Orthophoto generation (from textured meshes in real world coordinates to GeoTIFF)
```

### When doese label smoothing help by Hinton
论证了知识蒸馏+标签平滑是有用的，具体做法就是用硬标签先生成一个老师模型，再控制温度，训练一个基于软标签（label smoothing）的学生模型。因为之前的迁移学习、模型压缩不知道怎么把两种方法结合起来用，这篇paper提供了详尽的实验参考数据。


### Single-Stage Multi-Person Pose Machines
这是一篇One Stage 做姿态估计的文章，跟Realtime Multi-Person 2D Pose Estimation using Part Affinit Fields 类似， 不同点在于：
1. 它使用了Hourglass Network.
2. 它回归的内容为：Root joint Gaussian Heatmap, Normalized Displacements between the keypoints and the root joints.

如下图所示：
<img src="{{ site.github_cdn_prefix }}/screenshots/2020-02-13-17-55-48.png" class="img-ressponssive" style="width: 60%;margin-left: 3%">


对于第一个Target，就是普通的高斯Heatmap，这与大家回归普通关键点的方法一致。

对于第二个Target, 对于SMP， 是对图中的每个Person，先找到其Root Joints, 然后在Root Joints的范围是到当前点目标关键点的差，其他地方用mask不计算loss(这一点不确定)。HSMP类似。

然后就是实验结果：

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-02-13-17-29-50.png" class="img-ressponssive" style="width: 60%;margin-left: 3%">

这个实验结果本身存疑，其中的时间是58ms，这大概是Hourglass单次前传的时间，其中的PAF单次前传的时间大概在40ms+, mAP也在40+，但是这个Paper报告的PAF的是多尺度前传的时间（明显这样对比是不公平的）


### As-Projective-As-Possible Image Stitchingwith Moving DLT
使用单应性变换拼接图像的文章，据说是最早引入网格的文章之一，是后面的AANAP(Adaptive as-natural-as-possible image stitching)的基础，核心是用下面的滑动窗口最小二乘来描述图像之间的变换：

$$
    \mathbf{H}_* = \arg \min_\mathbf{h}\sum_{1}^{N}\parallel w_*^i \mathbf{A}_i \mathbf{h} \parallel \ s.t. \parallel\mathbf{h}\parallel = 1
$$

### 目标检测Reading list
1. cascade RCNN
2. 1st Place Solutions for OpenImage2019 - Object Detection and Instance Segmentation
3. IOU-Net
4. PrROI-Pooling
5. Double-Head RCNN
6. Double-Head-Ext
7. RefineDet
8. Reppoints / DCN v3
9. AlignDet

### Attention Is All You Need
论文链接：https://arxiv.org/abs/1706.03762

大名鼎鼎的Transformer， 笔记见<http://notes.kohill.cn/transformer>

### Self-Attention with Relative Position Representations
一篇基于Transformer 的论文

文章声称绝对位置是没有用的，相对位置更为重要，因此用相对位置编码而不是绝对位置编码，原始的Transformer的Attention如下：

$$z_{i}=\sum_{j=1}^{n} \alpha_{i j}\left(x_{j} W^{V}\right)$$

$$\alpha_{i j}=\frac{\exp e_{i j}}{\sum_{k=1}^{n} \exp e_{i k}}$$

$$ e_{i j}=\frac{\left(x_{i} W^{Q}\right)\left(x_{j} W^{K}\right)^{T}}{\sqrt{d_{z}}}$$

修改后的Attention 结构变为：

$$z_{i}=\sum_{j=1}^{n} \alpha_{i j}\left(x_{j} W^{V}+a_{i j}^{V}\right)$$

$$e_{i j}=\frac{x_{i} W^{Q}\left(x_{j} W^{K}+a_{i j}^{K}\right)^{T}}{\sqrt{d_{z}}}$$

其中$a_{i,j}^K$即位置编码，它与当前位置与其它位置的位置差有关，论文对这个相对位置做了clip，即
相对位置最大为8，超过8会被clip为8：

<img src="{{ site.github_cdn_prefix }}/transformer/2020-03-13-15-36-12.png" class="img-responsive"/>

对于$a_{i,j}^K$的学习，论文没有提怎么学的，但是目测就是靠一个embedding layer 学的。

具体实现的时候，self-attention 分别为Q和V，对于Q如下：
```python
        mul_left = mul_left[:, :, :, np.newaxis]  # (2, 8, 256, 1, 64)
        delta_x_embedded = delta_x_embedded.transpose((0, 1, 3, 2, 4))  # (2, 8, 256, 64, 256)
        delta_x_array = self.batch_dot(mul_left, delta_x_embedded).squeeze()

        delta_y_embedded = delta_y_embedded.transpose((0, 1, 3, 2, 4))  # (2, 8, 256, 64, 256)
        delta_y_array = self.batch_dot(mul_left, delta_y_embedded).squeeze()
```

对于V如下：

```python
        mul_left = mul_left[:, :, :, np.newaxis]
        delta_x_array = self.batch_dot(mul_left, delta_x_embedded).squeeze()
        delta_y_array = self.batch_dot(mul_left, delta_y_embedded).squeeze()
```

但有两点存疑：
1. 原文说学习一个$a_{i j}^{V}$，但是不清楚这个$a_{i j}^{V}$怎么来的（我是直接用一个nn.Embedding）。
2. 原文说overhead只有7%，但是我测下来，在每一个Encoder Layer上加一个position embedding 的开销相当大，
在只在第一个层和第二个层加入Relative Positio
n Embedding的情况下，训练速度只有原来的1/4，前传速度只有原来的1/25

### Character-Level Language Modeling with Deeper Self-Attention
论文链接：<https://www.aaai.org/ojs/index.php/AAAI/article/download/4182/4060>

文章对Transformer 架构做了一些改动
1. 增加了三个loss (序列的中间位置， hidden representations and multiple steps at target sequence in the future.) <br>
(1). Multiple Positions<br>
原文说transformer 只对最后一个单词算了loss，然后它改成了对每个位置都预测并且对每个位置都算loss(难道不应该本来就是这样子的嘛，很奇怪)
，该策略的增益为1.42，是所有策略中最大的<br>
(2) Intermedia Layer Losses<br>
就是让每一个Transformer layer 都直接预测序列，然后对于第$l^{th}$个中间层，若共有n个中间层，则在l/2n \times N个迭代周期后该中间层的loss 权重被置为0，也就是说，当训练进行到一半时，所有的中间层的loss都为0.， 该策略的增益为0.096<br>
(3) Multiple Targets<br>
网络同时预测多个目标，即再加一个fc同时预测下下一个字符，增益为0.006

有一点存疑：
训练的时候说是固定了512个字符，显然512是指Taget的长度，那么src的长度呢？


### Transformer-XL: Attentive Language ModelsBeyond a Fixed-Length Context
论文链接：<https://arxiv.org/pdf/1901.02860.pdf> <br>
代码链接：<https://github.com/kimiyoung/transformer-xl>

这篇文章主要diss的对象是<AAAI上的论文 Character-Level Language Modeling with Deeper Self-Attention>, 后者在训练的时候在语料库中随机采样固定长度的序列, 在前传的时候以滑动窗口的形式预测下一个字符。因为没有状态重用，每次预测的时候有很多重复计算。


这篇文章采用分段的形式，例如第一段的$h_1$，维度为(bs, seq_len, 512)，第二层concat上一段输出的隐含层,得到(bs, 2xseq_len, 512)的隐含状态，<font color=red>把上一段的第n层与当前段的第n+1层concat的好处是不用处理初始状态的问题</font>，此时网络可以公用上一段的信息，从而加速预测。

另外文章的一个观点是不能使用绝对位置编码（实际上文章的意思是段内的相对位置编码，不是整个输入的绝对位置编码）。此时不同段的相同位置的位置编码一致，因此会有问题。因此文章使用相对位置编码，注意此时Self Attention/Src Attention的输入包含上一段的信息，例如$x_{-1}, x_{-2}$, x1,x2是第一段的信息，x3,x4是第二段的信息，x4在计算相对位置编码的时候，对x3的相对位置是-1, 对x2的相对位置编码为-2, 对x1的相对位置编码是-3，默认情况下，并不会送入$x_{-1}, x_{-2}$。因此解决了位置编码confusing的问题。

此外，这篇文章对Self-Attention with Relative Position Representations这篇文章里的相对位置编码做了进一步改动，原始Transformer里的Attention Score为：

<img src="{{ site.github_cdn_prefix }}/transformer/2020-03-28-21-19-59.png" class="img-responsive"/>


其中$\mathbf{E}_{x_i}$是单词${x_i}$的embedding向量, $\mathbf{U}_j和\mathbf{U}_j$即位置编码。<br>
文章把它变为：

<img src="{{ site.github_cdn_prefix }}/transformer/2020-03-28-21-26-23.png" class="img-responsive"/>


其中$u^{\top}$为待学习的参数（向量），$\mathbf{R}_{i-j}$即相对位置编码，按文章的意思，上述每一项都有它的直观含义：

> Under  the  new  parameterization,  each  term  hasan intuitive meaning: term(a)represents content-based  addressing,  term(b)captures  a  content-dependent  positional  bias,   term(c)governs  aglobal content bias, and(d)encodes a global po-sitional bias.