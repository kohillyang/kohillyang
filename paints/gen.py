#coding=utf-8
import os

strbefore='''---
layout: default
---
<link rel="stylesheet" href="http://qcloud.kohill.cn/galleries/css/blueimp-gallery.css">
<link rel="stylesheet" href="http://qcloud.kohill.cn/galleries/css/blueimp-gallery-indicator.css">
<link rel="stylesheet" href="http://qcloud.kohill.cn/galleries/css/blueimp-gallery-video.css">

<div class="container main">
<center>
<span class="big-ornament">
  <img src="https://github.com/kohillyang/personal-blog/blob/master/logo.png?raw=true" style="width:10%">
</span>
</center>
<h2>Carousel video gallery</h2>
<!-- The Gallery as inline carousel, can be positioned anywhere on the page -->
<div id="blueimp-image-carousel" class="blueimp-gallery blueimp-gallery-carousel">
    <div class="slides"></div>
    <h3 class="title"></h3>
    <a class="prev"></a>
    <a class="next"></a>
    <a class="play-pause"></a>
</div>
<script src="http://qcloud.kohill.cn/galleries/js/blueimp-helper.js"></script>
<script src="http://qcloud.kohill.cn/galleries/js/blueimp-gallery.js"></script>
<script src="http://qcloud.kohill.cn/galleries/js/blueimp-gallery-indicator.js"></script>
<script src="http://qcloud.kohill.cn/galleries/js/blueimp-gallery-youtube.js"></script>
<script src="http://qcloud.kohill.cn/galleries/js/vendor/jquery.js"></script>
<script src="http://qcloud.kohill.cn/galleries/js/jquery.blueimp-gallery.js"></script>
<script type="text/javascript">
    var carouselLinks = []
'''
strafter='''
    blueimp.Gallery(carouselLinks, {
      container: '#blueimp-image-carousel',
      carousel: true
    })
</script>
</div>
'''
urlprefex="https://raw.githubusercontent.com/kohillyang/personal-blog/master/paints/"
urlsuffix=""
strformat='''
          carouselLinks.push({
            href: %s,
            title: %s
          })     
'''
def GetFileList(dir, fileList):
    for root, dirs, files in os.walk(dir): 
        fileList.extend(files)
    return fileList
fl = GetFileList('./', [])
findex = open("index.html","wt")
findex.write(strbefore)
for f in fl:
    if "png" in f or "jpg" in f:
        findex.write(strformat%("'"+urlprefex+f+urlsuffix+"'","'"+f+"'"))
    pass

findex.write(strafter)