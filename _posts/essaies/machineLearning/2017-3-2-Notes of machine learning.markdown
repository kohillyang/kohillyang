---
layout: post
title: Notes of machine learning
date: '2017-3-2 19:40'
comments: true
external-url: null
categories: machine%20learning
---

<br>

# 概要

1. 评分函数：将原始像素映射为分类评分值。
2. 损失函数：根据分类评分与训练集实际图像数据分类的一致性。有SVM与Softmax两种
3. 最优化：寻找$W$使得损失函数最小化。

## 资料链接

*[机器学习如何入门-知乎](https://www.zhihu.com/question/26006703)*

<https://zhuanlan.zhihu.com/p/21930884?refer=intelligentunit> 

<https://www.analyticsvidhya.com/blog/2015/06/tuning-random-forest-model/>

[关于SVM一篇比较全的博文](http://blog.csdn.net/v_july_v/article/details/7624837)

## k - Nearest Neighbor Classifier

Instead of finding the simple colsest image in the trainning set, finding the top k closet image, and voting on the label of the test image., By the end of this procedure, we could plot a graph that shows which values of k work best. We would then stick with this value and evaluate once on the actual test set.

Some method can be used to make the trainning process more fast.

- Approximate Nearest Neighbor (ANN)
- FLANN

**if u want to apply kNN in practice, some preprocess measuares should be used**

- Normalised the dataset to make them have zero mean and unit variance
- using some dimensionality reduction technology if the data is very high-dimensional.

## 符号说明
$x_i \in R^D$ each associated with a label $y_i$，we have $N$ examples(each with a dimensionality $D$)，and $K$ distinct categories.

score function: $f: R^D \mapsto R^K$ thart maps the raw image pixels to class scores.

**Linear classifier**

$f(x_i, W, b) =  W x_i + b$    $\,\,W$ corresponds to a *template*

Loss function $L_i$

Multiclass SVM loss for the i-th example:$L_i = \sum_{j\neq y_i} {\max(0, s_j - s_{y_i} + \Delta)}$, $s_j = f(x_i, W)_j$, $j$ means the j-th element.








## Image classification dataset

There's 60000 images with 50000 trainning set and a test set of 10000 images in [CIFAR-10](http://www.cs.toronto.edu/~kriz/cifar.html)

## 损失函数(Loss Function)

- 量化对分类标签的不满意程度

1. Multiclass Support Vector Machine Loss

$$L{i}=\sum{max(0,f+\Delta)}$$

1. L2_SVM(更常用):

$$L{i}={\sum{max(0,f+\Delta)}}^{2}$$

- Regularization Penalty(正则化惩罚)

权重并不是唯一的，假设权重$W$能正确分类，那么$kW$必定也能够正确分类，我们希望减少这种模糊性，从而引入正则化惩罚：

$$R_{W}=\sum{\sum{W_{k,l}^{2}}}$$

- 完整的损失函数

$${\frac{1}{N}}\sum_{i}{L_i}+\lambda{R_{W}}$$

其中前一项为损失函数，后一项为正则化惩罚，$\lambda$需要在交叉验证中选择。添加损失函数之后可以对最大数权重进行惩罚，从而提高其泛化能力。

**之后可以通过迭代，找到使得损失函数最小的权重$W$**

- 与支持向量机相关的其他算法
- Binary Support Vevtor Machine
- kernels，duals，SMO
- strategy: AVA(ALL VS ALL),OVA(One VS ALL)<br>
  虽然很多损失函数是不可微的，但这通常不会带来什么问题，因为可以使用`次梯度`。

## Softmax分类器

对于学习过`二元逻辑回归分类器`的读者来说，Softmax分类器就可以理解为逻辑回归分类器面对多个分类的一般化归纳

`交叉熵`

$$L_i=-log\frac{e^{f_{y_i}}}{\sum_{j}{e^{f_j}}}$$

Assume a training dataset of images $x_i \in R^D$, each associated with a label $y_i$.

交叉熵的输入是评分向量$f$，输出向量$L$。

与此有关的在神经连接中有个交叉熵代价函数：$-\frac{1}{n}\sum_{x}{[yln{a}+(1-y)ln(1-a)]}$

<ukw>Kullback-Leibler divergence</ukw>

衡量的是相同事件空间里的两个概率分布的差异情况。

## Softmax分类器与SVM之间的联系

- Softmax分类器最大化评分函数$f$中正确分类的分值与其他非正确分类分值的比值。
- SVM试图让正确分类比非正确分类高出一个 $\Delta$

The full Multiclass SVM loss becomes:

$$L = \underbrace{ \frac{1}{N} \sum_i L_i }_\text{data loss} + \underbrace{ \lambda R(W) }_\text{regularization loss}$$

但是在Softmax中交叉熵并不参与到评分计算中，它是在评分计算完成之后，计算评分正确与非正确之间的相对值作为损失函数的结果。

## 最优化

即梯度下降法，由于通常函数是不可微的，因此一般用数值得计算方法。用差分的方式计算往往效果更好：

$$\Delta=\frac{f(x+h)+f(x-h)}{2h}$$

缺点：在大规模计算中计算量太大，一般希望能获得微分的解析形式。

## 反向传播算法

反向传播算法用于从输出往相反方向计算局部梯度

## 神经网络

一个单层的神经网络如下：

$$s=W_{2}{max(0,W_1{x})}$$

值得注意的是$max$是一个非线性函数，这个非线性是非常重要的，否则它将会退化成一个线性函数。

类似的，一个三层的神经网络可以看成： $$W_{3}max(0,W_2{max(0,W_1{x})})$$

## 激活函数

Sigmoid函数将输入压缩到(0,1)

$$\sigma = \frac{1}{1+e^{-x}} $$

tanh函数将输入压缩到(-1,1)

ReLU函数

$$f(x)=max(0,x)$$

![]({{ site.github_cdn_prefix }}/articleImages/20170303.png)

上图是是ReLU（校正线性单元：Rectified Linear Unit）激活函数，当x=0时函数值为0。当x>0函数的斜率为1，[论文](http://link.zhihu.com/?target=http%3A//www.cs.toronto.edu/%7Efritz/absps/imagenet.pdf)指明使用ReLU比使用tanh的收敛快6倍。

## 神经网络对数据分类的演示

<http://cs.stanford.edu/people/karpathy/convnetjs/demo/classify2d.html>

## 奇异值分解以及主成分分析

```python
# 假设输入数据矩阵X的尺寸为[N x D]
X -= np.mean(X, axis = 0) # 对数据进行零中心化(重要)
cov = np.dot(X.T, X) / X.shape[0] # 得到数据的协方差矩阵
```

主成分分析只保留数据中方差较大的分量，而忽略其中方差较小的分量，以实现数据降维。

通常使用PCA降维过的数据训练线性分类器和神经网络会达到非常好的性能效果，同时还能节省时间和存储器空间。

## 白化

<div class="alert alert-warning">
数据预处理中，计算得到的平均值应该只是训练集合的平均值。在测试中，应该用测试集减去由训练集得到的平均值。
</div>

最后一个在实践中会看见的变换是白化（whitening）。白化操作的输入是特征基准上的数据，然后对每个维度除以其特征值来对数值范围进行归一化。该变换的几何解释是：如果数据服从多变量的高斯分布，那么经过白化后，数据的分布将会是一个均值为零，且协方差相等的矩阵。该操作的代码如下：

```python
# 对数据进行白化操作:
# 除以特征值
Xwhite = Xrot / np.sqrt(S + 1e-5)
#分母中添加了1e-5（或一个更小的常量）来防止分母为0
```

## 关于梯度查错的一些技巧

1. 使用中心化公式
    $$\frac{f(x)}{x}=\frac{f(x+h)-f(x-h)}{2h}$$ 相对于标准定义的情况，中心化的误差小一个数量级 3. 比较数值梯度与解析梯度的时候使用相对误差而不是绝对误差
2. 使用双精度
3. 寻找特定情况下的正确损失值
4. 对小数据子集过拟合
5. 跟踪损失函数值
6. 如果数据是图像数据，那么可以对第一层进行可视化

## 其他一些更新方法

1. 梯度下降法
    $$x= x -\text{learning_rate}_grad$$ - 动量更新
    $$v = v+m_u_v -\text{learning_rate}*grad$$ $$x = x+v$$ - Nesterov动量
- 学习率退火：在一段时间后让学习率渐渐降低是比较重要的，几种公式如下：
   $$\alpha={\alpha}_{0}e^{-kt}$$ $$\alpha=\frac{\alpha_{0}}{1+kt}$$ 5. 牛顿法以及以牛顿法为基础的比如L-BFGS之类的方法
6. Adagrad,RMSprop,Adam等自适应学习算法
7. 超参数搜索中使用对数参数范围

## 卷积神经网络

对于普通的神经网络，每一层映射关系：

$$y=f(x)$$
式中$x,y$都是向量

对于卷积神经网络络，每一层映射关系：

$$B=f(A)$$
$B,A$
都是三维的，即每一层把一个三维的数据映射到另外一个三维数据

三种主要的层： 卷积神经网络有三种主要的层：卷积层，汇聚（Pooling）层和全连接层。

- 卷积层

- 卷积层的连接是局部连接，卷积层的深度是和数据的深度是一致的。

- `在深度方向上可以由很多神经元。`这些神经元接接收数据的相同部分，也即`感受野`相同，被称为$depth column$，也有人称之为$fibre$.
- 卷积神经网络的每个神经单元本质上是一个二维FIR滤波器，滤波器不断滑动步长$step$，权重与输入数据做卷积得到输出，所以输出是一张二维图。增大步长$step$可以减小神经元输出的数量，大于3的$step$很少用。
- 保证输入数据的尺寸可以使用$zero-padding$
- 输出数据体在空间上的尺寸可以通过输入数据体尺寸（W），卷积层中神经元的感受野尺寸（F），步长（S）和零填充的数量（P）的函数来计算。假设输入数组的空间形状是正方形，即高度和宽度相等）输出数据体的空间尺寸为(W-F +2P)/S+1。比如输入是7x7，滤波器是3x3，步长为1，填充为0，那么就能得到一个5x5的输出。如果步长为2，输出就是3x3。
- 汇聚层

- 汇聚层主要用于降采样，它会把大量的激活信息丢掉

- 最大汇聚，在以步长$S$递增每个$F*F$的区域中取最大值，通常$S$为2，$F$也为2。当$S<F$时成为重叠汇聚。
- 除了最大汇聚之外，还有`L2-norm pooling`以及`平均汇聚`，平均汇聚较少用。

- 归一化层 归一化层如今很少用了

- 全连接层

- 在两种变换中，将全连接层转化为卷积层在实际运用中更加有用

### 核函数
RBF Kernel



### 常用分类器
<http://blog.csdn.net/july_sun/article/details/53088673>

传统的机器学习的监督学习分类分类和回归，分类是争对离散的数据，而回归是争对连续的数据，在数据预处理好的基础上要对数据进行预测，通常采用CV交叉验证来进行模型评价和选择。这篇文章通过连续的数据结合sklearn库对各种回归器做一比较：<br>
1. linear regression<br>
缺点：顾名思义，linear regression是假设数据服从线性分布的，这一假设前提也限制了该模型的准确率，因为现实中由于噪声等的存在很少有数据是严格服从线性的。<br>
优点：基于这种假设，linear regression可以通过normal equation求闭合解的方式求得y_predict<br>
2. logistic regression<br>
缺点：从线性回归衍生而来，将线性的值域通过sigmoid函数压缩在（0,1）范围内，缺点同linear regression，且也是要求数据是无缺失的<br>
优点：有两种方式求解，精确的解析解和SGD算法估计，在要求准确性时使用解析解，在要求时间效率时使用SGD 迭代<br>
3. SVM（支持向量机 ）<br>
缺点：计算代价比较大，SVM是将低维无序杂乱的数据通过核函数（RBF,poly，linear，sigmoid）映射到高维空间，通过超平面将其分开<br>
优点：SVM是通过支撑面做分类的，也就是说不需要计算所有的样本，高维数据中只需去少量的样本，节省了内存<br>
在sklearn默认配置中三种核函数的准确率大概是：RBF>poly>linear<br>
4. Naive Bayes<br>
缺点：这一模型适合用在文本样本上，采用了朴素贝叶斯原理假设样本间是相互独立的，因此在关联比较强的样本上效果很差<br>
优点：也是基于其独立的假设，概率计算大大简化，节省内存和时间<br>
5. K近邻<br>
缺点：k需要人为设定，且该算法的复杂度很高<br>
优点：“近朱者赤，近墨者黑”KNN是无参数训练的模型<br>
6. 决策树（DT）<br>
缺点：在训练数据上比较耗时<br>
优点：对数据要求度最低的模型，数据可以缺失，可以是非线性的，可以是不同的类型，，最接近人类逻辑思维的模型，可解释性好<br>
7. 集成模型（众志成城模型）<br>
random forest：随机抽取样本形成多个分类器，通过vote，少数服从多数的方式决定最终属于多数的分类器结果，分类器之间是相互去之间关联的<br>
gradient boost：弱弱变强，最典型的代表是adaboost（三个臭皮匠，顶个诸葛亮），弱分类器按照一定的计算方式组合形成强的分类器，分类器之间存在关联，最终分类是多个分类器组合的结果<br>
一般地，GB>RF>DT<br>
但是集成模型缺点在于受概率的影响，具有不确定性<br>

以上是常用的回归分类器的比较，在知道各种分类器的优缺点之后就可以使用正确的分类器完成自己的数据处理，如下表是通过计算各类分类器的残差来对比同一任务不同分类器之间的好坏，可以看出来在sklearn默认参数的前提下，准确率排序是：集成模型>DT>SVM>KNN>Linear<br>

| 分类回归器        | 导入python库命令    导入函数命令  | 残差（%）|
 --------   | -----:   | ----: | ------:|
|linear regression	| from sklearn.linear_model import LinearRegressor	lr = LinearRegressor()	| 5.223
|SGD regression penalty L2  |  from sklearn.linear_model import SGDRegressor	SGDR = SGDRegressor("penalty = l2") |	5.780
|SGD regression penalty L1	|  SGDR = SGDRegressor("penalty = l1")	| 5.765
|SVR(rbf kernel)	| from sklearn .svm import SVR （Penalty parameter ：C，Kernel coefficient ：gamma）	SVR = SVR(kernel="rbf")	| 0.627
|SVR(sigmoid kernel)	| SVR = SVR(kernel="sigmoid ")	| 82.507
|SVR(poly kernel)	| SVR = SVR(kernel="poly")	| 20.862
|SVR(linear kernel)	| SVR = SVR(kernel="linear")	| 6.451
|KNN（n=5，weights=uniform）	| from sklearn.neighbors import KNeighborsRegressor	knn = KNeighborsRegressor（n=5，weights="uniform"）	| 0.731
|KNN（n=5，weights=distance）	| knn = KNeighborsRegressor（n=5，weights="distance"）| 	1.087
|Random forest	| from sklearn.ensemble import RandomForestRegressor	RF = RandomForestRegressor()	| 0.270
|DT	 | from sklearn.tree import DecisionTreeRegressor	DT = DecisionTreeRegressor()	| 0.447
|Extra Trees	| from sklearn.ensemble import ExtraTreesRegressor	ET = ExtraTreesRegressor()	| 0.246
|Gradient Boosting	| from sklearn.ensemble import GradientBoostingRegressor	GB = GradientBoostingRegressor()	| 0.284

### Points
> We can of course, train models such as linear regression and support vector machines with gradient descent too, and in fact this is common when the training set is extremely large.

当线性回归或者支持向量机模型涉及的训练数据过大时，通常也是使用梯度向量迭代。
> In most cases, our parametric model defines a distribution p(y | x;θ) and we simply use the principle of maximum likelihood. This means we use the cross-entropy between the training data and the model’s predictions as the cost function.

`交叉熵 cross-entropy`，衡量的是事件空间中两个概率空间的分布情况。
<div class ="alert alert-info">大多数情况下，参数模型定义的是条件概率分布：$p(y | x;θ)$</div>

> Most modern neural networks are trained using maximum likelihood
>
<div class ="alert alert-info">现代的很多神将网络都是使用极大似然来训练参数。</div>



### Problems
> This means that neural networks are usually trained by using iterative, gradient-based optimizers that merely drive the cost function to a very low value, rather than the linear equation solvers used to train linear regression models or the convex optimization algorithms with global convergence guarantees used to train logistic regression or SVMs

<div class ="alert alert-info">这说明逻辑回归或者是SVM是线性分类器？？？</div>

## TF-IDF特征
TF：针对某个词hello，统计某个单词在该文档中出现的概率

$$P_{tf}=\frac{单词在该文档中出现的次数}{\text{该文档的单词总数}}$$

IDF：针对某个词，统计该词在所有文档中出现比率再取对数
$$P_{idf}=\frac{\sum_{i}^N{1(单词在文档i中出现) }}{N}$$
其中N为总文档数

则有：
$$\text{TF-IDF}=P_{tf}\times ln{P_{idf}}$$
