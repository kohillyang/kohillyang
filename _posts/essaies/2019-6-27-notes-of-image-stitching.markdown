---
layout: post
title: Image Stitching
date: 2019-6-27 3:15
comments: true
external-url:
categories: 杂文
permalink: /image_stitch
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


### Jau 30th 结果

用colmap重建出的点云经过重采样后的结果

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-30-22-54-03.png" class="img-responsive" style="width:80%;margin-left:2%"/><br>


使用泊松表面重建的结果

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-30-23-02-35.png" class="img-responsive" style="width:80%;margin-left:2%"/><br>

使用delaunay三角化进行表面重建的结果

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-30-23-04-11.png" class="img-responsive" style="width:80%;margin-left:2%"/><br>

效果比使用泊松表面重建要好上不少，但是很多地方有毛刺

如果直接对上面的点云使用法线贴图：

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-30-23-05-43.png" class="img-responsive" style="width:80%;margin-left:2%"/><br>

因为毛刺的存在，其实效果并不是很好：

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-30-23-07-40.png" class="img-responsive" style="width:80%;margin-left:2%"/><br>

目前正在尝试寻找使用moving least square 来对点云进行平滑， 一个参考资料为:
<http://www.pointclouds.org/assets/files/presentations/ICCV2011-surface.pdf>

<img src="{{ site.github_cdn_prefix }}/screenshots/2020-01-31-00-33-50.png" class="img-responsive" style="width:80%;margin-left:2%"/><br>

两张图片拼接代码：
```python
import cv2 as cv
import cv2
import numpy as np
box = cv.imread("/data3/zyx/yks/eclipse_workspace/moving_dlt/left/2000.jpg");
box = np.rot90(box, 1)
box_in_sence = cv.imread("/data3/zyx/yks/eclipse_workspace/moving_dlt/left/2144.jpg");
box_in_sence = np.rot90(box_in_sence, 1)

cv.imshow("box", box)
cv.imshow("box_in_sence", box_in_sence)

# ??ORB?????
orb = cv.ORB_create()
kp1, des1 = orb.detectAndCompute(box,None)
kp2, des2 = orb.detectAndCompute(box_in_sence,None)

canvas = box.copy()
result_kp0 = cv.drawKeypoints(canvas, kp1, None, -1, cv.DrawMatchesFlags_DEFAULT)
cv.imwrite("result_kp0.jpg", result_kp0)
canvas = box_in_sence.copy()
result_kp1 = cv.drawKeypoints(canvas, kp2, None, -1, cv.DrawMatchesFlags_DEFAULT)
cv.imwrite("result_kp1.jpg", result_kp1)

# ???? ?????????
# FLANN_INDEX_KDTREE = 1
# index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
# search_params = dict(checks = 50)
# flann = cv.FlannBasedMatcher(index_params, search_params)
# matches = flann.knnMatch(des1,des2,k=2)

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1,des2)

good = matches
# for m,n in matches:
#     if m.distance < 0.7*n.distance:
#         good.append(m)
img1 = box
img2 = box_in_sence
src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
matchesMask = mask.ravel().tolist()
h,w,d = img1.shape
pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
dst = cv.perspectiveTransform(pts,M)
img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
cv.imshow("img2", img2)


def create_mask(img1, img2, version):
    height_img1 = img1.shape[0]
    width_img1 = img1.shape[1]
    width_img2 = img2.shape[1]
    height_panorama = height_img1
    width_panorama = width_img1 + width_img2
    offset = int(200 / 2)
    barrier = img1.shape[1] - int(200 / 2)
    mask = np.zeros((height_panorama, width_panorama))
    if version == 'left_image':
        mask[:, barrier - offset:barrier + offset] = np.tile(np.linspace(1, 0, 2 * offset).T, (height_panorama, 1))
        mask[:, :barrier - offset] = 1
    else:
        mask[:, barrier - offset:barrier + offset] = np.tile(np.linspace(0, 1, 2 * offset).T, (height_panorama, 1))
        mask[:, barrier + offset:] = 1
    return cv2.merge([mask, mask, mask])

def blending(H, img1, img2):
    # H = self.registration(img1, img2)
    height_img1 = img1.shape[0]
    width_img1 = img1.shape[1]
    width_img2 = img2.shape[1]
    height_panorama = height_img1
    width_panorama = width_img1 + width_img2

    panorama1 = np.zeros((height_panorama, width_panorama, 3))
    mask1 = create_mask(img1, img2, version='left_image')
    panorama1[0:img1.shape[0], 0:img1.shape[1], :] = img1
    panorama1 *= mask1
    mask2 = create_mask(img1, img2, version='right_image')
    panorama2 = cv2.warpPerspective(img2, H, (width_panorama, height_panorama)) * mask2
    result = panorama1 + panorama2

    rows, cols = np.where(result[:, :, 0] != 0)
    min_row, max_row = min(rows), max(rows) + 1
    min_col, max_col = min(cols), max(cols) + 1
    final_result = result[min_row:max_row, min_col:max_col, :]
    return final_result

stitched = blending(M, box_in_sence.copy(), box.copy())
cv.imshow("", stitched.astype(np.uint8))
cv.waitKey(0)
# ????
result = cv.drawMatches(box, kp1, box_in_sence, kp2, matches, None)
cv.imwrite("match.png", result)
cv.imshow("orb-match", result)
cv.waitKey(0)
cv.destroyAllWindows()
```