---
layout: post
title: C Plus Plus
date: 2017-4-18 19:40
comments: true
external-url:
categories: cpp
---
<br>

[GCC优化选项](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html)

### gcc编译选项之DEBUG

```
-g  Produce debugging information in the operating system’s native format (stabs, COFF, XCOFF, or DWARF 2).  GDB can work with this debugging 
           information.

-gstabs 
          Produce debugging information in stabs format (if that is supported), without GDB extensions.  This is the format used by DBX on most BSD 
          systems.  On MIPS, Alpha and System V Release 4 systems this option produces stabs debugging output which is not understood by DBX or SDB.  On 
          System V Release 4 systems this option requires the GNU assembler.

-gstabs+ 
           Produce debugging information in stabs format (if that is supported), using GNU extensions understood only by the GNU debugger (GDB).  The use 
           of these extensions is likely to make other debuggers crash or refuse to read the program.

-ggdb 
           Produce debugging information for use by GDB.  This means to use the most expressive format available (DWARF 2, stabs, or the native format if 
           neither of those are supported), including GDB extensions if at all possible.

-g目测与-ggdb等同，与gdb兼容性最好
-gstabs+ 测试能读到源代码，但是不能执行表达式
-gstabs 没作测试
-
```

### Makefile的几种赋值语句

```bash
= 是最基本的赋值
:= 是覆盖之前的值
?= 是如果没有被赋值过就赋予等号后面的值
+= 是添加等号后面的值
```

### C语言中的 %le %lf %lg
输出的时候：
1. %le 默认指数输出
2. %lf 默认小数形式输出
3. %lg 自动选择
输入的时候目测没有区别。

### C语言的几种文件打开方式
1. "r"，只读方式
2. "w"，只写，如果文件存在，文件会被清空。如果文件不存在，则创建一个新文件
3. "a", append，如果文件存在，则所有的写操作都会被追加到文件末尾

### 一个简单的Makefile 模板

```bash
#$@ is the name of the file being generated, and 
#$< the first prerequisite (usually the source file). 
```

```Makefile
PATH:=../mingw530_32/bin;$(PATH);

headers=api.h FFT.h FileDwt.h MelCal.h 
sources=fft.cpp fileDwt.cpp MelCal.cpp melcof.cpp xu.cpp
INCFLAGS = -I./inc
CPPFLAGS = -Og  $(INCFLAGS) -Wall -Wno-strict-aliasing -shared -std=c++14
LINKFLAGS = 
CPP = g++

dll_name=melcal.dll
vpath %.h ./inc
vpath %.dll ../pythonsrc/



all: $(dll_name) 
$(dll_name) : $(sources) $(headers) 

  $(CPP) -v
  $(CPP) $(CPPFLAGS) $(sources) -o $(dll_name) $(LINKFLAGS)
clean:
  rm -f $(dll_name)
.PHONY : clean all
```

### string与wstring的相互转换
```cpp
  std::string WstringToString(const std::wstring str)
  {// wstring转string
      unsigned len = str.size() * 4;
      setlocale(LC_CTYPE, "");
      char *p = new char[len];
      wcstombs(p,str.c_str(),len);
      std::string str1(p);
      delete[] p;
      return str1;
  }
```


### Makefile 编译Qt

Makefile 如下
```bash

PRO   = test.pro
QMAKE = D:\PortableProgram\Qt5.8\5.8\mingw53_32\bin\qmake.exe

all:  QtMakefile
  $(MAKE) -f QtMakefile

clean:
  rm -fr QtMakefile QtMakefile.debug QtMakefile.release debug release

QtMakefile:
  $(QMAKE) -o QtMakefile $(PRO) CONFIG+=debug_and_release

debug:  QtMakefile
  $(MAKE) -f QtMakefile debug

release:  QtMakefile
  $(MAKE) -f QtMakefile release

.PHONY: all clean debug clean-debug release clean-release
```
test.pro文件如下：

```
#include "DateTime.h"
#include <QtGui/QGuiApplication>
#include <QtQuick/QtQuick>
int main( int argc, char * argv[] )
{
    QGuiApplication app(argc, argv);
    DateTime datetime;
    QQuickView view;
    view.rootContext()->setContextProperty( "datetimeModel", &datetime );
    view.setSource( QStringLiteral( "src/test.qml" ) );
    view.show();
    app.connect( view.engine(), SIGNAL( quit() ), SLOT( quit() ) );
    return app.exec();
}
```
