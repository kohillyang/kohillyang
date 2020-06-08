---
layout: post
title: 英语模板
date: 2019-5-20 17:32
comments: true 
external-url:
categories: linux
permalink: /ideas
---
<br>


### 评审意见
This paper deals with the challenging weak scratch detection problem for optical components. The main contribution is that a convolutional neural network fusing scale attention and channel attention has been proposed. This new network can help generate pretty useful attention-aware features which are missing in many existing deep learning based weak scratch detection methods. Experimental results show that the scratch detection performance has been significantly improved compared with the traditional and current deep learning-based methods. It is suggested to accept this paper subject to some minor revisions as listed below.
 
1. The BA module in this paper is more like a simpler histogram equalization method for contrast enhancement. It is not learnable and inappropriate to call it a module and hard attention. Usually Hard/Soft in CNN means that the weight is either a binary number or a real number between zero and one. This is a bit confusing.
2. It is unreasonable to use F1 to evaluate the performance of different models in this paper. A more reasonable metric is to use ROC, or the largest F1.
3. It is necessary to compare the proposed method in this paper with the more general state-of-the-art object detection method, e.g., Cascade R-CNN. The RetinaNet compared in this paper is not a state-of-the-art method.