---
layout: post
title: 关于Python调用C的开销
date: '2017-5-8 19:40'
comments: true
external-url: null
categories: python
---
<br>

### 关于Python 调用C语言的开销
测试并不严谨，但是还是有参考价值的。

作为测试，C语言代码如下（仅仅测试之用）:

```cpp
#include <stdint.h>
#include <cmath>
#include <stdlib.h>
#include <stdio.h>
extern "C"  double add(double a, double b);
extern "C" double dlog(double x);
extern "C" double add(double x, double y){
    return x * y * x *x * y*x * y * x *x * y*x * y * x *x * y*x * y * x *x * y;  
}

extern "C" double dlog(double x){
    if (x<0){
        printf("%lf\n",x );
        exit(-1);
    }
    return std::log(x);
}
```

Makefile如下：

```bash
#export PATH:=E:\ProgramData\WinPython-64bit\scripts;E:\ProgramData\WinPython-64bit\python-3.5.3.amd64;E:\ProgramData\WinPython-64bit\python-3.5.3.amd64\Scripts;$(PATH);
PATH:=D:\PortableProgram\Qt5.8\Tools\mingw530_32\bin;$(PATH);
dll_name=add.dll
all:$(dll_name) hashtest.py
	"D:\Program Files (x86)\WinPython-32bit-3.4.3.5\python-3.4.3\python.exe" hashtest.py
	
headers= 
sources=add.cpp
INCFLAGS = -I./
CPPFLAGS = -O2  $(INCFLAGS) -Wall -Wno-strict-aliasing -shared -std=c++14
LINKFLAGS = 
CPP = g++

$(dll_name) : $(sources) $(headers) 
	$(CPP) $(CPPFLAGS) $(sources) -o $(dll_name) $(LINKFLAGS)
clean:
	rm -f $(dll_name)
.PHONY : clean all	
```

O2优化下生成dll

Python代码如下:
```python
#Pylint: skip-file
from ctypes import CDLL,c_int32,c_double
import time
import math as npp
dll = CDLL("add.dll")
add = dll.add
add.argtypes=[c_double,c_double]
add.restype = c_double
dlog = dll.dlog
dlog.argtypes = [c_double]
dlog.restype = c_double

lx = lambda x,y:x * y * x *x * y*x * y * x *x * y*x * y * x *x * y*x * y * x *x * y
pre = list(range(1,1000000))
final = list(map(lambda x: abs(hash(x))+1,pre))
final2 = list(map(lambda x: abs(hash(x))+1,pre))
t0 = time.time()

final3 = map(lambda x,y:add(x,y),final,final2)
print(sum(map(lambda x:dlog(x),final3)))
t1 = time.time()
final4 = map(lx,final,final2)
print(sum(map(lambda x:npp.log(x),final4)))
t2 = time.time()
print(t1-t0,t2-t1)
```

所做的事情很简单：求对数，求和

输出：

```bahs
g++ -O2  -I./ -Wall -Wno-strict-aliasing -shared -std=c++14 add.cpp -o add.dll
"D:\Program Files (x86)\WinPython-32bit-3.4.3.5\python-3.4.3\python.exe" hashtest.py
256310367.69315302
256310367.69315302
2.6453800201416016 2.931102991104126
```

python 耗时2.93s,C语言2.64s，两者几乎持平。

这表示，当函数至少有超过20次运算时，用C写才可能比较划算。

如果C只做一次+运算呢，输出如下：

```
"D:\Program Files (x86)\WinPython-32bit-3.4.3.5\python-3.4.3\python.exe" hashtest.py
13508664.872070571
13508664.872070571
2.564340829849243 0.5728890895843506
```

C语言的开销并没有减少多少，但是使用python的开销就只有原来的1/6。

结论就是，Python下调用C函数每1000000次调用会有2.5s的固定开销（与具体函数运算无关）。而Python在1000000下的函数调用开销大概为0.4s，所以Python比C快6倍。