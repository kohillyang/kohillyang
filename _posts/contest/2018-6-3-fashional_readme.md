---
layout: post
title: fashion ai readme.md
date: 2018-6-3 19:40
comments: true
external-url:
categories: presentation
---


### 概述
代码共使用了两个模型, DRN50+GCN,DRN101+GCN在最终的heatmap上按0.5，0.5的权重加权平均融合，得到heatmap之后取最大值点作为最终模型的输出，模型训练过程中没有使用外部数据集，训练环境为8x Tesla P40 + E5-2690，从零开始训练需要3天，在决赛时，前传使用8张P40需要5个小时。提交的前传代码在不改变结果的情况下做了少量速度优化，预计单张m40需要45h.

### 模型简介
1. DRN50+GCN
编码器部分采用带孔Resnet50，主要参考代码为<https://github.com/fyu/drn>和<https://arxiv.org/abs/1705.09914>，解码器部分采用GCN，代码主要来源为<https://github.com/zijundeng/pytorch-semantic-segmentation>，参考论文为<https://arxiv.org/pdf/1703.02719>，模型结构文件名为`models/gcn.py`，模型参数大小为146.4MB,模型参数存储在`output/DRN_GCN`中, 在前传时采用了swa策略，参考论文为<https://arxiv.org/abs/1803.05407>，即在目录中存储了多份模型参数，实际模型参数大小应等于单个文件大小。
2. DRN101+GCN
DRN101+GCN与DRN50+GCN基本相同，不同之处为编码器为带孔Resnet101，模型存储在`output/DRN_GCN_101`中，模型参数大小为222.7MB。
3. 模型输出
模型输出为24个类别的高斯图，对每个类别的高斯图取argmax得到具体坐标。


