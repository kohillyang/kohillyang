---
layout: post
title: human post detect
date: '2017-9-11 19:40'
comments: true
external-url: null
categories: machine-learning
---
<br>
```bash
sudo apt-get install -y build-essential cmake pkg-config
sudo apt-get install -y libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python2.7-dev python3.5-dev
```
<br>

<https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation><br>
<https://github.com/anewell/pose-hg-train><br>
<https://github.com/tensorboy/pytorch_Realtime_Multi-Person_Pose_Estimation><br>
<https://github.com/bearpaw/pytorch-pose><br>
<https://github.com/bearpaw/pose-attention><br>


[人体姿态识别领域年度进展报告](http://mp.weixin.qq.com/s?__biz=MzI1NTE4NTUwOQ==&mid=2650326421&idx=1&sn=bec1bd90da6b8a624ad68272cedb0afe&chksm=f235a29fc5422b89ddb473002080420f761c73047d8dcf274f5959dabf36be366dd8126da072&mpshare=1&scene=1&srcid=0910x7MgVU6BnOZbH7TJeCrG#rd)


[全球AI挑战赛](https://challenger.ai/)



<div><img src="{{ site.github_cdn_prefix }}/screenshots/2017-9-11-001.png" class="img-responsive center-block" style="width:33%;flow:left"></div>

1. input image: w x j
2. score via PAF（A set of 2D vector that encode the location and orientation of limbs over the image domain）
3. * body part confidence S S_j(w x h), one per part.
   * part affinities L L_c(w x h x 2),  one per limb.
4. Two branches: confidence map branch, affinity fields
5. the image is first initialized by a finetuned VGG-network, which generate a set of feature map F.
6. Each stage, Each brach has been applied a loss function.
7. L2 Loss between the estinmated predictions and ground truth maps.
8.


介绍了一种避免梯度弥散的方法（周期性地补偿）
[31] S.-E. Wei, V. Ramakrishna, T. Kanade, and Y. Sheikh. Convolutional pose machines. In CVPR, 2016. 1, 2, 3, 6
