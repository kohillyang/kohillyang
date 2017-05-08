---
layout: post
title: notes of pic.md
date: 2017-06-03 19:40
comments: true
external-url:
categories: linux
---
<br>

## 型号：PIC18F2585
<http://www.microchip.com/wwwproducts/en/PIC18F2585>
PIC18F2585与PIC18F2580的区别在于RAM大小和主频大小不同

```
PIC18F系列单片机最好使用PICC编译器，因为MCC18编译效果不如PICC

PIC单片机的UART与其他单片机很不同，这点请注意，特别是发送

说实话pic的i2c是最没方圆的


对于PIC，各个不同型号的相同资源，其使用基本是相同的。

在C18安装目录下面的UART和IIC例程，一般都是基本通用的
```
C18编译器下载地址<http://www.microchip.com/Developmenttools/ProductDetails.aspx?PartNO=SW006011>已失效？？？

不过根据说明，只兼容C89啊，居然不支持C99,Sad……

目测只需要在MPLAB的菜单中设置即可（Select Language Toolsuite-> Active Toolsuite）

*安装最好在末尾选中添加到环境变量中*，这样是不是可以直接打make编译？？

MPLAB® Code Configurator

<http://www.microchip.com/mplab/mplab-code-configurator>

MPLAB® Code Configurator (MCC) is a free, graphical programming environment that generates seamless, easy-to-understand C code to be inserted into your project. Using an intuitive interface, it enables and configures a rich set of peripherals and functions specific to your application.

MPLAB Code Configurator supports 8-bit, 16-bit and 32-bit PIC® microcontrollers. MCC is incorporated into both the down-loadable MPLAB X IDE and the cloud based MPLAB Xpress IDE.

<!-- MPLAB® Harmony Integrated Software Framework
<http://www.microchip.com/mplab/mplab-harmony>
MPLAB® Harmony is a flexible, abstracted, fully integrated firmware development platform for PIC32 microcontrollers. It takes key elements of modular and object oriented design, adds in the flexibility to use a Real-Time Operating System (RTOS) or work without one, and provides a framework of software modules that are easy to use, configurable for your specific needs, and that work together in complete harmony.

MPLAB Harmony includes a set of peripheral libraries, drivers and system services that are readily accessible for application development. The code development format allows for maximum re-use and reduces time to market. -->

MPLAB® XC Compilers

<http://www.microchip.com/mplab/compilers>


## 安装步骤
1. 安装MAPLAB IDE
2. 安装XC 编译器
3. 安装插件，在Tools -> 中选择code configurator
4. 添加库支持（在Tools->Options->Plugin->add Library）

<http://www.studentcompanion.co.za/mplab-code-configurator/>
PIC18的似乎已经被称为Legacy Peripheral Libraries了？？？
上面的办法行不通了？？？
总之要安装Legacy Peripheral Libraries，下载链接为<http://www.microchip.com/mplab/compilers>，藏的比较深，慢慢找吧

