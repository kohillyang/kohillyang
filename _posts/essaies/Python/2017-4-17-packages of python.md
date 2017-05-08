---
layout: post
title: packages of python
date: '2017-4-17 19:40'
comments: true
external-url: null
categories: python
---
<br>

本文的目的在于整理一些比较好用的python packages

### Glmnet
Glmnet is a package that fits a generalized linear model via penalized maximum likelihood. The regularization path is computed for the lasso or elasticnet penalty at a grid of values for the regularization parameter lambda. The algorithm is extremely fast, and can exploit sparsity in the input matrix  x. It fits linear, logistic and multinomial, poisson, and Cox regression models. A variety of predictions can be made from the fitted models. It can also fit multi-response linear regression。

目测是关于线性回归方面的一个集合包（不懂）。

<https://web.stanford.edu/~hastie/glmnet/glmnet_alpha.html#intro>

### gensim
[gensim](http://radimrehurek.com/gensim/tutorial.html)
似乎自带Word2Vec？不知道效果好不好。
似乎是一个文本挖掘的库，自带tf-idf？那我还为啥自己写？

或许之前的朴素贝叶斯如果用近义词之类的可能稍微提高精度吧

### prettytable
[rettytable](https://code.google.com/p/prettytable/)
托管在GoogleCode。prettytable主要用于在终端或浏览器端构建很好的输出。

### progressbar
[progressbar](https://code.google.com/p/python-progressbar/)
是一个进度条库，该库提供了一个文本模式的progressbar。 

### colorama
[colorama](https://pypi.python.org/pypi/colorama)主要用来给文本添加各种颜色，并且非常简单易用。

### bashplotlib
[bashplotlib](https://github.com/glamp/bashplotlib)bashplotlib是一个绘图库，它允许你使用stdin绘制柱状图和散点图等。 

### Curses
Python 下的一个控制控制台的库，可以改一下颜色位置之类的
<https://www.zhihu.com/question/21100416>

突然想到linux下的nano 似乎依赖libcursor这个库，想来也是用来实现各种颜色控制的功能的。

### shelve
Python下用来放任意数据类型的字典（只不过数据不是放在内存中，而是在硬盘里）。之前用mysql封装了一个类似的，不过在随机存取的时候性能不高，但是只读取或者插入的时候还是挺快的（每秒上万次插入吧……）。

pickle在dump的时候似乎会申请比较多的内存……，这个要注意

### scp
Python 下传输文件的一个包
<https://github.com/jbardin/scp.py>


```python
from paramiko import SSHClient
from scp import SCPClient

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('example.com')

with SCPClient(ssh.get_transport()) as scp:
	scp.put('test.txt', 'test2.txt')
```

### paramiko
<http://www.cnblogs.com/yangmv/p/5169924.html>

<http://www.cnblogs.com/ma6174/archive/2012/05/25/2508378.html>

可以用来做远程登陆

```python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,22,username,passwd,timeout=5)
for m in cmd:
    stdin, stdout, stderr = ssh.exec_command(m)
    
#           stdin.write("Y")   #简单交互，输入 ‘Y’ 
    out = stdout.readlines()
    #屏幕输出
    for o in out:
        print (o),
ssh.close()
```

paramiko还自带了ssh客户端，可以用来传输文件之类，不过需要服务端支持

```python
import paramiko

t = paramiko.Transport((“主机”,”端口”))
t.connect(username = “用户名”, password = “口令”)
sftp = paramiko.SFTPClient.from_transport(t)
remotepath=’/var/log/system.log’
localpath=’/tmp/system.log’
sftp.put(localpath,remotepath)
t.close()
```


### random
random.shuffle (lst)
对lst随机排序,shuffle:洗牌