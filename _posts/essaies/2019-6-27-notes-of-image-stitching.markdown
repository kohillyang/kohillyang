---
layout: post
title: Image Stitching
date: 2019-6-27 3:15
comments: true
external-url:
categories: 杂文
---
<br>
### libelas
    给定两张图片，这个库可以给出视差图

### 多视图几何参考书籍：
    参考https://zhuanlan.zhihu.com/p/34995102
	《Multiple View Geometry in Computer Vision (Second Edition)》
	
###  状态估计参考论文
	state estimation for robotics

### 三维空间优化
	Lie groups, Lie algebras, projective geometry and optimization for 3D Geometry, Engineering and Computer Vision

### 四元数动力学
	https://arxiv.org/pdf/1711.02508.pdf
	Quaternion kinematics for the error-state Kalman filter

### Optimal Ray Intersection For Computing 3D Points From N-View Correspondences
Optimal Ray Intersection For Computing 3D Points From N-View Correspondences

Python 实现代码：
```Python
def triangulatePoints(list_of_re_projection_matrix, list_of_mn):
    # type: ([np.ndarray], [np.ndarray]) -> np.ndarray
    sum_A = np.zeros(shape=(3, 3))
    sum_b = np.zeros(shape=(3, 1))
    for J, mn in zip(list_of_re_projection_matrix, list_of_mn):
        assert J.shape == (3, 4)
        assert mn.shape == (2, 1)
        mn_homo = np.ones(shape=(3, 1))
        mn_homo[:2, :] = mn[:2, :]
        KR = J[:3, :3]
        KR_inv = np.linalg.inv(KR)
        Kt = J[:3, 3:4]
        l = KR_inv.dot(mn_homo)
        l = l / np.sqrt(np.sum(l ** 2))
        q = -1 * KR_inv.dot(Kt)
        a = l[0].squeeze().tolist()
        b = l[1].squeeze().tolist()
        c = l[2].squeeze().tolist()
        x = q[0].squeeze().tolist()
        y = q[1].squeeze().tolist()
        z = q[2].squeeze().tolist()
        sum_A += np.array([[1 - a ** 2, -1 * a * b, -1 * a * c],
                           [-1 * a * b, 1 - b ** 2, -1 * b * c],
                           [-1 * a * c, -1 * b * c, 1 - c ** 2]])
        sum_b += np.array([[(1 - a ** 2) * x - a * b * y - a * c * z],
                           [-1 * a * b * x + (1 - b ** 2) * y - b * c * z],
                           [-1 * a * c * x - b * c * y + (1 - c ** 2) * z]])
    x = np.linalg.inv(sum_A).dot(sum_b)
    return x
```

### 经典论文
`1`. <http://matthewalunbrown.com/papers/ijcv2007.pdf>

### SFM常用软件
`1`. pmvs<br>
`2`. Smart3D <http://www.zhdrtk.com/3528.html>


### 开源代码
`1` 2016 STOF: [colmap](https://github.com/colmap/colmap)， [论文链接](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Schonberger_Structure-From-Motion_Revisited_CVPR_2016_paper.pdf)<br>
`2`. [OpenPano](https://github.com/ppwwyyxx/OpenPano)


### 相机位姿的另外一种解法
考虑相机模型：
$$s_0p_0=KP \\ s_1p_1=K(RT+P)   $$<br>
上式的几何意义是在空间中的一条直线，直线在空间中的自由度为5，因此，上式可改写成：<br>
$$
    \begin{cases}
        x_0 = s_0 \times sin\theta_0 cos \phi_0 \\
        y_0 = s_0 \times sin \theta_0 sin \phi_0  \\
        z_0 = s_0 \times cos \theta_0       
    \end{cases}
$$
<br>
$$
    \begin{cases}
        x_1 = \Delta x + s_1 \times sin(\theta_1 + \Delta \theta) cos (\phi_1 + \Delta \phi) \\
        y_1 = \Delta y + s_1 \times sin(\theta_1 + \Delta \theta) sin (\phi_1 + \Delta \phi)  \\
        z_1 = \Delta z + s_1 \times cos (\theta_1 + \Delta \theta)       
    \end{cases}
$$

假设两幅图像共$K$个匹配的关键点，记$D_k$为如下的矩阵：<br>
$$
D_k = \left[ \begin{matrix}
    sin\theta_0 cos \phi_0                                   & sin \theta_0 sin \phi_0                                  & cos \theta_0  \\
    sin(\theta_1 + \Delta \theta)cos (\phi_1 + \Delta \phi)  & sin(\theta_1 + \Delta \theta) sin (\phi_1 + \Delta \phi) & cos (\theta_1 + \Delta \theta)  \\
    \Delta x                                                 & \Delta y                                                 & \Delta z
\end{matrix} \right]
$$
<br>
则\ref{equa:camera_line0}和\ref{equa:camera_line1}两条直线的距离为:<br>
$$
d_k = |det(D_k)|    
$$

直观上来讲，上式所表示的物理意义为： 空间中的两条直线，若它们相交，则距离一定为0，与其交点无关；若不相交，则其公垂线段的中点与公垂线段的长度无关。<br>

对于共$K$个匹配对的情况，我们希望求出来的相机位姿能最小化$\sum_{k=1}^K d_k^2$。<br>
对式子\ref{equa:2_15}展开：<br>
$$
D_k = sin\theta_0 cos \phi_0 \times sin(\theta_1 + \Delta \theta) sin (\phi_1 + \Delta \phi) \times \Delta z - sin\theta_0 cos \phi_0 \times \Delta y \times cos (\theta_1 + \Delta \theta)\\
    - sin \theta_0 sin \phi_0 sin(\theta_1 + \Delta \theta)cos (\phi_1 + \Delta \phi) \Delta z +  sin \theta_0 sin \phi_0 \times \Delta x \times cos (\theta_1 + \Delta \theta) \\
    +   cos \theta_0 sin(\theta_1 + \Delta \theta)cos (\phi_1 + \Delta \phi) \Delta y -  cos \theta_0  \Delta x  sin(\theta_1 + \Delta \theta) sin (\phi_1 + \Delta \phi) 
$$


