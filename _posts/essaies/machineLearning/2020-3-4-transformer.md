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


? beam search算分数的时候，需要考虑到<END>
当出现<END>时，分数乘以1而不是当前分数