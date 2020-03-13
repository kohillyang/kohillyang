---
layout: post
title: Notes of transformer
date: 2019-3-4 10:24
comments: true
permalink: /transformer
categories: machine-learning
---
<br>
整体框架：

<img src="{{ site.github_cdn_prefix }}/transformer/Total.svg" class="img-responsive"/>

编码器：

<img src="{{ site.github_cdn_prefix }}/transformer/Encoder_layer.svg" class="img-responsive"/>

解码器：

<img src="{{ site.github_cdn_prefix }}/transformer/Decoder_layer.svg" class="img-responsive"/>

Attention:

<img src="{{ site.github_cdn_prefix }}/transformer/Attention.svg" class="img-responsive"/>


1. 输入图片加入mask
2. 随机非gt训练
3. label smooth
4. 增加一个branch, 加入CTC Loss辅助训练
5. generator 与 target 共享encoding<https://arxiv.org/abs/1608.05859>
6. sub word list <https://github.com/rsennrich/subword-nmt>
7. Double Check beam search
8. Model Average
9. 金字塔，多个尺度拼接成一张图片往里面送
10. Embedding 使用Normal(0, 1/sqrt(len(dim))) 初始化而不是Xavier(Ps. Embedding 目前使用的mxnet的自带默认初始化方法，并不是用的Xavier)
11. Deformable
12. 相关位置Encoding https://arxiv.org/pdf/1803.02155.pdf， PS：多尺度不work的原因很可能与该文章有关。
13. beam search算分数的时候，需要考虑到<END>, 当出现<END>时，分数乘以1而不是当前分数

关于论文Self-Attention with Relative Position Representations<https://arxiv.org/pdf/1803.02155.pdf>：

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