---
layout: post
title: Linux
date: 2017-02-13 19:40
comments: true
external-url:
categories: linux
permalink: /linux
---
<br>

### 三种分布式存储

分布式存储的应用场景相对于其存储接口，现在流行分为三种:对象存储: 也就是通常意义的键值存储，其接口就是简单的GET、PUT、DEL和其他扩展，如七牛、又拍、Swift、S3块存储: 这种接口通常以QEMU Driver或者Kernel Module的方式存在，这种接口需要实现Linux的Block Device的接口或者QEMU提供的Block Driver接口，如Sheepdog，AWS的EBS，青云的云硬盘和阿里云的盘古系统，还有Ceph的RBD（RBD是Ceph面向块存储的接口）文件存储: 通常意义是支持POSIX接口，它跟传统的文件系统如Ext4是一个类型的，但区别在于分布式存储提供了并行化的能力，如Ceph的CephFS(CephFS是Ceph面向文件存储的接口)，但是有时候又会把GFS，HDFS这种非POSIX接口的类文件存储接口归入此类。

作者：hermitBaby
链接：https://www.zhihu.com/question/21536660/answer/79458092
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


### N2N VPN
windows安装包<http://www.vpnhosting.cz/n2nguien.exe>

windows版本supernode似乎填域名不能正常运行，改成填ip地址就好了。

linux 源代码项目地址<https://github.com/meyerd/n2n/branches>

win下很简单，打开exe，单击advanced按键，勾选Enable packet forwarding through n2n community，其他的默认不用勾选。

OpenWrt 下(似乎还有luci-app版本，反正我的有)

```bash
opkg update && opkg install n2n
```

### 在linux上搭建私有git服务器
<http://www.tuicool.com/articles/VRrI7fe>


### 创建回环设备

几点说明：
1. losetup -f 查看空闲回环设备
2. kpartx 映射分区（或者叫读取分区）,比如<pre>kpartx -av /dev/loop0</pre>
3. 对于可以启动的img文件，可以以以下命令启动：
4. kpartx 映射出来设备在/dev/mapper下找

<pre>
sudo kvm  --bios  ./OVMF.fd /dev/sdb -net nic,model=ne2k_pci -net user -soundhw es1370 -serial stdio
</pre>

```bash
dd if=/dev/zero of=openwrt-uefi.img bs=2048M count=1 #创建一个空文件
losetup -f #查看空闲回环设备
losetup /dev/loop4 test.img #挂在回环设备
fdisk /dev/loo4 #对回环设备进行分区
kpartx -av test.img #读取分区
mkfs.ext4 /dev/loo4p1 #格式化分区
mount /dev/mapper/loo4p1 /mnt #挂载分区
umount /mnt #卸载分区
kpartx -dv /dev/loop4 #
losetup -d /dev/loop4
```

### nmap 端口扫描
nmap -p 3389 10.0.0.101


### grub2-install
```bash
 losetup -fP disk1
 ls /dev/loop0*
 #   /dev/loop0  /dev/loop0p1  /dev/loop0p2  /dev/loop0p3
 mount /dev/loop0p1 /mnt
 cat > loop0device.map <<EOF
 (hd0) /dev/loop0
 EOF
 grub-install --no-floppy --grub-mkdevicemap=loop0device.map --modules="part_msdos" --boot-directory=/mnt /dev/loop0 -v
 umount /mnt
losetup -d /dev/loop0
qemu-system-x86_64 -m 512 -curses -hda disk1 -enable-kvm
```


### 文件管理器
nautilus


### grub2 可以加的启动参数列别
<https://www.mjmwired.net/kernel/Documentation/kernel-parameters.txt>

### linux字体全家桶
<https://github.com/chrissimpkins/codeface>


### 转socks5代理为http代理
<http://blog.csdn.net/li740207611/article/details/52045471>
<https://blog.phpgao.com/privoxy-shadowsocks.html>

简单来说就是中介Privoxy把socks5转为http代理，只需要设置监听的端口和地址以及上层代理的地址即可。

wget 设置代理

```bash
export http_proxy='http://localhost:8118'
export https_proxy='http://localhost:8118'
```


### linux 下运行linux出错
<https://bugs.launchpad.net/ubuntu/+source/swt-gtk/+bug/975560>

```
java.lang.UnsatisfiedLinkError: Could not load SWT library. Reasons:
 no swt-pi-gtk-3740 in java.library.path
 no swt-pi-gtk in java.library.path

My java version:
java version "1.7.0"
Java(TM) SE Runtime Environment (build 1.7.0-b147)
Java HotSpot(TM) 64-Bit Server VM (build 21.0-b17, mixed mode)

Already tried the following:

"sudo apt-get install libswt-gtk-3-java
```
原因是没有装图形
`sudo apt-get install libswt-gtk-3-java`

### linux 中DISPLAY变量的作用
默认情况下，为了安全，默认启动的xserver中是不监听TCP端口的
```bash
deepin@deepin-pc:~$ ps -aux | grep xorg
root       572  4.3  1.7 445696 140424 tty7    Ssl+ 15:20   9:18 /usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt7 -novtswitch
deepin   10596  0.0  0.0  14528   960 pts/5    S+   18:55   0:00 grep xorg
```
这可以在`/etc/X11/xinit/xserverrc`中更改
```bash
deepin@deepin-pc:~$ cat /etc/X11/xinit/xserverrc
#!/bin/sh

exec /usr/bin/X -nolisten tcp "$@"
```
另外一种更通用的做法是打开SSHd的X11forward选项(`/etc/ssh/ssh_config`)
```bash
Host *
#   ForwardAgent no
    ForwardX11 yes
```
之后可以远程开启桌面之类
```bash
DISPLAY=192.168.1.166:0.0 startx &
DISPLAY=:0 gedit
sudo apt-get -u install x-window-system-core
sudo apt-get -u install gdm gdm-themes
sudo apt-get -u install kde-core kde-i18n-zhcn
```

### easybcd引导deepin
```
title install  deepin-15
find --set-root /deepin.iso
kernel /vmlinuz  findiso=/deepin.iso  noprompt quiet splash  boot=live ro deepin-installer/locale=zh_CN.UTF-8 keyboard-configuration/layoutcode=us keyboard-configuration/variantcode= --  rootflags=sync auto-deepin-installer
initrd /initrd.lz
boot
```


### 关于在linux下编译RTL8821AU出现错误的解决办法：
因为某些原因，x86中移除了is_compat_task这个函数
<https://patchwork.kernel.org/patch/8116411/>

```bash
[ 1102.035160] usb 1-1.3: Manufacturer: Realtek
[ 1102.035161] usb 1-1.3: SerialNumber: 00e04c000001
[ 1102.072474] 8821au: Unknown symbol is_compat_task (err 0)
[ 1637.461839] 8821au: Unknown symbol is_compat_task (err
```

解决办法是
`#define is_compat_task in_compat_syscall`



### linux 挂载sftp磁盘

```bash
m_yzl:
	sshfs yzl@192.168.31.8:/home/yzl/yangkeshan/ yzl
m_hszc:
	sshfs hszc@192.168.31.88:/home/hszc/yangkeshan hszc
umount:
	-fusermount -u yzl
	-fusermount -u hszc
```
### winsshfs
windows下的sshfs
<https://segmentfault.com/a/1190000009439697>
<https://github.com/Foreveryone-cz/win-sshfs/releases>
开源软件，应该比netdrivex之类的好使

### deepin安装cuda
<http://blog.csdn.net/liaodong2010/article/details/71482304>
亲测成功


### Eclipse调试ROS
- 使用roscd packagename 切换到包的目录
- 使用命令cmake -G"Eclipse CDT4 - Unix Makefile"创建Eclipse工程
- 执行cmake  -DCMAKE_BUILD_TYPE=Debug  设置编译器为调试模式

- 在Eclipse中使用Import导入工程
- 在Eclipse中配置ROS_ROOT ROS_MASTER_URL等变量
- 新建debug选项


### linux 格式化json文件
当json文件非常庞大的时候，用下面的命令格式化json比较好
```bash
sudo apt install jq
cat abc.json | jq . > format.json
```


### linux Qt工程出现
```bash
l_visualizer
This application failed to start because it could not find or load the Qt platform plugin "xcb"
in "".
```
有两种办法解决这个问题：
1. 复制Qt的platform文件夹到二进制文件目录
2. export QT_QPA_PLATFORM_PLUGIN_PATH=/media/deepin/software/Qt5.8.0/5.8/gcc_64/plugins


### install nvidia-cuda using cuda-8.0
`sudo nvidia-docker run --rm nvidia/cuda:8.0-devel nvidia-smi`<br>
`nvidia-docker run -itd --name=data1 -v /data1/yks:/data1/yks nvidia/cuda:8.0-devel /bin/bash`

### fix window maximum bug in x2go.
The windows would flash in some cases, see <https://github.com/ArcticaProject/nx-libs/issues/600><br>
Updating VcXsrv to 1.19.4 or newer will fix this bug.<br>
<https://sourceforge.net/projects/vcxsrv/files/vcxsrv/1.19.6.4/vcxsrv-64.1.19.6.4.installer.exe/download>


### force umounting sshfs directory.
My current workaround is to:<br>
Find the culprit sshfs process:<br>
`pgrep -lf sshfs` <br>
Kill it:<br>
`kill -9 <pid_of_sshfs_process>`<br>
sudo force unmount the "unavailable" directory:<br>
`sudo umount -f <mounted_dir>`<br>
Remount the now "available" directory with sshfs ... and then tomorrow morning go back to step 1.

```cpp
//设置PB输出0，PA开漏输出1
PB = 0;
PA = 0xff;
// 读取PA
uint8_t tmp1 = PA;
uint8_t tmp2 = 0;
for(int i = 0;i<4;i++){
	PB = 1<<i;
	if (tmp1 != PA){
		tmp2 = i;
	}
}		
```

### 强制apt使用IPv6/IPv4
快速命令行选项
如果只想一次使apt-get使用IPv4或IPv6，使用下列步骤。该功能尽在apt-get的0.9.7.9~exp1版本后可用。首先，通过如下命令确认apt-get版本高于0.9.7.9~exp1：

`apt-get --version`
结果近似于:

`apt 1.0.1ubuntu2 for amd64 compiled on Oct 28 2014 20:55:14`
版本核实后，可以通过如下命令强制使用IPv4:

`apt-get -o Acquire::ForceIPv4=true update`
或IPv6:

`apt-get -o Acquire::ForceIPv6=true update`
这会将sources.list中的URL仅解析成IPv4并更新仓库。

持久化的选项
为了让设置持久化，在/etc/apt/apt.conf.d/下创建99force-ipv4文件。

`sudoedit /etc/apt/apt.conf.d/99force-ipv4`
在该文件放入如下内容：

`Acquire::ForceIPv4 "true";`


### 查看各大主流机房延迟
<http://cloudping.bastionhost.org>

![](assets/screenshots/2018-06-08-10-13-49.png)


### linux 内核开发中查看module的结构体首地址
`cat /proc/kallsyms | grep _this_module | grep module_name`<br>

### 查看已安装的软件包
`apt list --installed | grep opencv`

### 记一次编译出现的错误
在编译ORB-SLAM的时候，大概出现了下面的而错误
```
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFIsTiled@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFOpen@LIBTIFF_4.0'
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFReadEncodedStrip@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFSetField@LIBTIFF_4.0'
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFWriteScanline@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFGetField@LIBTIFF_4.0'
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFScanlineSize@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFSetWarningHandler@LIBTIFF_4.0'
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFSetErrorHandler@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFReadEncodedTile@LIBTIFF_4.0'
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFReadRGBATile@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFClose@LIBTIFF_4.0'
/usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference to TIFFRGBAImageOK@LIBTIFF_4.0' /usr/lib/gcc/x86_64-linux-gnu/4.8/../../../x86_64-linux-gnu/libopencv_highgui.so: undefined reference toTIFFReadRGBAStrip@LIBTIFF_4.0'
```

主要怀疑的点有：
1. 没有装tiff，经检查装了libtiff5-dev,且有libtiff.so
2. opencv版本不对，使用命令`apt list --installed | grep opencv`检查opencv版本，确保只有一个版本的opencv，并卸载所有经过编译安装的opencv
3. 依赖项配置不正确，最后发现是Pangolin单独链接了anaconda的tiff，与系统的tiff冲突。
   


### Qt for ARM 移植
1. 下载Qt的源码，我选择的是5.12.4, 此过程大概需要1h
![](assets/screenshots/2019-7-29-10-04-01.png)
![](assets/screenshots/2019-7-29-09-57-01.png)
2. 解压工具链，我解压到了`/home/kk/arm-himix200-linux`
3. 运行`sudo ./arm-himix200-linux.install `安装工具链
4. 测试下工具链是否安装成功

```bash
kk@heils-server:/media/kk/data/kk/3516DV300/arm-himix200-linux$ arm-himix200-linux-gcc -v
Using built-in specs.
COLLECT_GCC=arm-himix200-linux-gcc
COLLECT_LTO_WRAPPER=/opt/hisi-linux/x86-arm/arm-himix200-linux/host_bin/../libexec/gcc/arm-linux-gnueabi/6.3.0/lto-wrapper
Target: arm-linux-gnueabi
Configured with: /home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/src/gcc-6.3.0/configure --host=i386-redhat-linux --build=i386-redhat-linux --target=arm-linux-gnueabi --prefix=/home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/install --enable-threads --disable-libmudflap --disable-libssp --disable-libstdcxx-pch --with-gnu-as --with-gnu-ld --enable-languages=c,c++ --enable-shared --enable-lto --enable-symvers=gnu --enable-__cxa_atexit --disable-nls --enable-clocale=gnu --enable-extra-hisi-multilibs --with-sysroot=/home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/install/target --with-build-sysroot=/home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/install/target --with-gmp=/home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/obj/host-libs/usr --with-mpfr=/home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/obj/host-libs/usr --with-mpc=/home/sying/SDK_CPU_UNIFIED/build/script/arm-himix200-linux/arm_himix200_build_dir/obj/host-libs/usr --enable-libgomp --disable-libitm --enable-poison-system-directories --with-pkgversion='HC&C V100R002C00B027_20181107'
Thread model: posix
gcc version 6.3.0 (HC&C V100R002C00B027_20181107) 
```
<https://blog.csdn.net/vickycheung3/article/details/82182136>

1. 修改`/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/mkspecs/linux-arm-gnueabi-g++/qmake.conf`
> 这里修改了两个地方，一是定义了arm的架构，其中：QT_QPA_PLATFORM是指定QPA平台的插件，这里选择的是linuxfb，参数-O是编译器提供的优化选项，如-O、-O1、-O2、-O3等，代表不同的优化级别，参数-march后面指定的是目标处理器的架构（可能指定不同的架构会调用不同的指令集，猜的~）；另外一个改动的地方就是将下面g++.conf和linux.conf中的参数值中加上了fsl，如arm-none-linux-gnueabi-gcc，这是我选择的交叉编译器，可以根据自身的情况修改。

原始版本：
```bash
#
# qmake configuration for building with arm-linux-gnueabi-g++
#

MAKEFILE_GENERATOR      = UNIX
CONFIG                 += incremental
QMAKE_INCREMENTAL_STYLE = sublib

include(../common/linux.conf)
include(../common/gcc-base-unix.conf)
include(../common/g++-unix.conf)

# modifications to g++.conf
QMAKE_CC                = arm-linux-gnueabi-gcc
QMAKE_CXX               = arm-linux-gnueabi-g++
QMAKE_LINK              = arm-linux-gnueabi-g++
QMAKE_LINK_SHLIB        = arm-linux-gnueabi-g++

# modifications to linux.conf
QMAKE_AR                = arm-linux-gnueabi-ar cqs
QMAKE_OBJCOPY           = arm-linux-gnueabi-objcopy
QMAKE_NM                = arm-linux-gnueabi-nm -P
QMAKE_STRIP             = arm-linux-gnueabi-strip
load(qt_config)
```

修改后的版本：
```bash
#
# qmake configuration for building with arm-linux-gnueabi-g++
#

MAKEFILE_GENERATOR      = UNIX
CONFIG                 += incremental
QMAKE_INCREMENTAL_STYLE = sublib

QT_QPA_PLATFORM= linuxfb:fb=/dev/fb0
QMAKE_CFLAGS_RELEASE += -Og -g -march=armv7-a
QMAKE_CXXFLAGS_RELEASE += -Og -g -march=armv7-a

include(../common/linux.conf)
include(../common/gcc-base-unix.conf)
include(../common/g++-unix.conf)

# modifications to g++.conf
QMAKE_CC                = arm-himix200-linux-gcc
QMAKE_CXX               = arm-himix200-linux-g++
QMAKE_LINK              = arm-himix200-linux-g++
QMAKE_LINK_SHLIB        = arm-himix200-linux-g++

# modifications to linux.conf
QMAKE_AR                = arm-himix200-linux-ar cqs
QMAKE_OBJCOPY           = arm-himix200-linux-objcopy
QMAKE_NM                = arm-himix200-linux-nm -P
QMAKE_STRIP             = arm-himix200-linux-strip
load(qt_config)
```

2. 执行
```bash
./configure -v -prefix /media/kk/data/kk/3516DV300/Qt-install -release -make libs -xplatform linux-arm-gnueabi-g++ -optimized-qmake -pch -qt-zlib -no-opengl -no-sse2 -no-openssl -no-cups -no-separate-debug-info -nomake examples -nomake tools

直接`make && make install `
会出现下面的错
<pre>
arm-himix200-linux-g++ -c -include .pch/Qt5Quick -pipe -Og -g -march=armv7-a -Og -g -march=armv7-a -O2 -std=c++1y -fvisibility=hidden -fvisibility-inlines-hidden -fno-exceptions -Wall -W -Wvla -Wdate-time -Wshift-overflow=2 -Wduplicated-cond -D_REENTRANT -fPIC -DQT_NO_URL_CAST_FROM_STRING -DQT_NO_INTEGER_EVENT_COORDINATES -DQT_NO_FOREACH -DQT_NO_NARROWING_CONVERSIONS_IN_CONNECT -DQT_BUILD_QUICK_LIB -DQT_BUILDING_QT -DQT_NO_CAST_TO_ASCII -DQT_ASCII_CAST_WARNINGS -DQT_MOC_COMPAT -DQT_USE_QSTRINGBUILDER -DQT_DEPRECATED_WARNINGS -DQT_DISABLE_DEPRECATED_BEFORE=0x050000 -DQT_NO_EXCEPTIONS -D_LARGEFILE64_SOURCE -D_LARGEFILE_SOURCE -DQT_NO_DEBUG -DQT_GUI_LIB -DQT_QML_LIB -DQT_NETWORK_LIB -DQT_CORE_LIB -DQT_NETWORK_LIB -DQT_CORE_LIB -I. -I. -I../../include -I../../include/QtQuick -I../../include/QtQuick/5.12.4 -I../../include/QtQuick/5.12.4/QtQuick -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtGui/5.12.4 -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtGui/5.12.4/QtGui -I../../include/QtQml/5.12.4 -I../../include/QtQml/5.12.4/QtQml -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtCore/5.12.4 -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtCore/5.12.4/QtCore -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtGui -I../../include/QtQml -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtNetwork -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/include/QtCore -I.moc -I/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/mkspecs/linux-arm-gnueabi-g++ -o .obj/qtquick2.o qtquick2.cpp
In file included from socketcanbackend.cpp:37:0:
socketcanbackend.h:83:5: error: 'canfd_frame' does not name a type
     canfd_frame m_frame;
</pre>

### Qt 5.9.5 for ARM 移植
`1`. 下载源码：
<pre>
wget https://mirrors.tuna.tsinghua.edu.cn/qt/archive/qt/5.9/5.9.5/single/qt-everywhere-opensource-src-5.9.5.tar.xz
tar -xf qt-everywhere-opensource-src-5.9.5.tar.xz
</pre>

`2`. 修改`/media/kk/data/kk/3516DV300/Qt/5.12.4/Src/qtbase/mkspecs/linux-arm-gnueabi-g++/qmake.conf`
> 这里修改了两个地方，一是定义了arm的架构，其中：QT_QPA_PLATFORM是指定QPA平台的插件，这里选择的是linuxfb，参数-O是编译器提供的优化选项，如-O、-O1、-O2、-O3等，代表不同的优化级别，参数-march后面指定的是目标处理器的架构（可能指定不同的架构会调用不同的指令集，猜的~）；另外一个改动的地方就是将下面g++.conf和linux.conf中的参数值中加上了fsl，如arm-none-linux-gnueabi-gcc，这是我选择的交叉编译器，可以根据自身的情况修改。

原始版本：
```bash
#
# qmake configuration for building with arm-linux-gnueabi-g++
#

MAKEFILE_GENERATOR      = UNIX
CONFIG                 += incremental
QMAKE_INCREMENTAL_STYLE = sublib

include(../common/linux.conf)
include(../common/gcc-base-unix.conf)
include(../common/g++-unix.conf)

# modifications to g++.conf
QMAKE_CC                = arm-linux-gnueabi-gcc
QMAKE_CXX               = arm-linux-gnueabi-g++
QMAKE_LINK              = arm-linux-gnueabi-g++
QMAKE_LINK_SHLIB        = arm-linux-gnueabi-g++

# modifications to linux.conf
QMAKE_AR                = arm-linux-gnueabi-ar cqs
QMAKE_OBJCOPY           = arm-linux-gnueabi-objcopy
QMAKE_NM                = arm-linux-gnueabi-nm -P
QMAKE_STRIP             = arm-linux-gnueabi-strip
load(qt_config)
```

修改后的版本：
```bash
#
# qmake configuration for building with arm-linux-gnueabi-g++
#

MAKEFILE_GENERATOR      = UNIX
CONFIG                 += incremental
QMAKE_INCREMENTAL_STYLE = sublib

QT_QPA_PLATFORM= linuxfb:fb=/dev/fb0
QMAKE_CFLAGS_RELEASE += -Og -g -march=armv7-a
QMAKE_CXXFLAGS_RELEASE += -Og -g -march=armv7-a

include(../common/linux.conf)
include(../common/gcc-base-unix.conf)
include(../common/g++-unix.conf)

# modifications to g++.conf
QMAKE_CC                = arm-himix200-linux-gcc
QMAKE_CXX               = arm-himix200-linux-g++
QMAKE_LINK              = arm-himix200-linux-g++
QMAKE_LINK_SHLIB        = arm-himix200-linux-g++

# modifications to linux.conf
QMAKE_AR                = arm-himix200-linux-ar cqs
QMAKE_OBJCOPY           = arm-himix200-linux-objcopy
QMAKE_NM                = arm-himix200-linux-nm -P
QMAKE_STRIP             = arm-himix200-linux-strip
load(qt_config)
```

`3`. 执行
```bash
./configure -v -prefix /media/kk/data/kk/3516DV300/Qt-install -release -make libs -xplatform linux-arm-gnueabi-g++ -optimized-qmake -pch -qt-zlib -no-opengl -no-sse2 -no-openssl -no-cups -no-separate-debug-info -nomake examples -nomake tools -gstreamer 1.0 
```
<!-- 这儿有个细节，我额外加了一个static 的参数，这样Qt在编译可执行文件的时候，会将所有的依赖全部编译到一个可执行文件中，而不用附带很多so文件。 -->
注意如果加上static 选项的话，在使用Qt的plugin的时候（例如linuxfb），需要静态导入插件，具体可见<https://doc.qt.io/qt-5/plugins-howto.html>

配置结果
```bash
Building on: linux-g++ (x86_64, CPU features: mmx sse sse2)
Building for: linux-arm-gnueabi-g++ (arm, CPU features: <none>)
Configuration: cross_compile compile_examples enable_new_dtags largefile precompile_header release c++11 c++14 c++1z concurrent dbus no-pkg-config reduce_exports release_tools static stl
Build options:
  Mode ................................... release; optimized tools
  Optimize release build for size ........ no
  Building shared libraries .............. no
  Using C++ standard ..................... C++1z
  Using ccache ........................... no
  Using gold linker ...................... no
  Using new DTAGS ........................ yes
  Using precompiled headers .............. yes
  Using LTCG ............................. no
  Target compiler supports:
    NEON ................................. no
  Build parts ............................ libs
Qt modules and options:
  Qt Concurrent .......................... yes
  Qt D-Bus ............................... yes
  Qt D-Bus directly linked to libdbus .... no
  Qt Gui ................................. yes
  Qt Network ............................. yes
  Qt Sql ................................. yes
  Qt Testlib ............................. yes
  Qt Widgets ............................. yes
  Qt Xml ................................. yes
Support enabled for:
  Using pkg-config ....................... no
  QML debugging .......................... yes
  udev ................................... no
  Using system zlib ...................... no
Qt Core:
  DoubleConversion ....................... yes
    Using system DoubleConversion ........ no
  GLib ................................... no
  iconv .................................. yes
  ICU .................................... no
  Logging backends:
    journald ............................. no
    syslog ............................... no
    slog2 ................................ no
  Using system PCRE2 ..................... no
Qt Network:
  getaddrinfo() .......................... yes
  getifaddrs() ........................... yes
  IPv6 ifname ............................ yes
  libproxy ............................... no
  OpenSSL ................................ no
    Qt directly linked to OpenSSL ........ no
  SCTP ................................... no
  Use system proxies ..................... yes
Qt Gui:
  Accessibility .......................... yes
  FreeType ............................... yes
    Using system FreeType ................ no
  HarfBuzz ............................... yes
    Using system HarfBuzz ................ no
  Fontconfig ............................. no
  Image formats:
    GIF .................................. yes
    ICO .................................. yes
    JPEG ................................. yes
      Using system libjpeg ............... no
    PNG .................................. yes
      Using system libpng ................ no
  EGL .................................... no
  OpenVG ................................. no
  OpenGL:
    Desktop OpenGL ....................... no
    OpenGL ES 2.0 ........................ no
    OpenGL ES 3.0 ........................ no
    OpenGL ES 3.1 ........................ no
  Session Management ..................... yes
Features used by QPA backends:
  evdev .................................. yes
  libinput ............................... no
  INTEGRITY HID .......................... no
  mtdev .................................. no
  tslib .................................. no
  xkbcommon-evdev ........................ no
QPA backends:
  DirectFB ............................... no
  EGLFS .................................. no
  LinuxFB ................................ yes
  VNC .................................... yes
  Mir client ............................. no
Qt Widgets:
  GTK+ ................................... no
  Styles ................................. Fusion Windows
Qt PrintSupport:
  CUPS ................................... no
Qt Sql:
  DB2 (IBM) .............................. no
  InterBase .............................. no
  MySql .................................. no
  OCI (Oracle) ........................... no
  ODBC ................................... no
  PostgreSQL ............................. no
  SQLite2 ................................ no
  SQLite ................................. yes
    Using system provided SQLite ......... no
  TDS (Sybase) ........................... no
Qt SerialBus:
  Socket CAN ............................. yes
  Socket CAN FD .......................... no
QtXmlPatterns:
  XML schema support ..................... yes
Qt QML:
  QML interpreter ........................ yes
  QML network support .................... yes
Qt Quick:
  Direct3D 12 ............................ no
  AnimatedImage item ..................... yes
  Canvas item ............................ yes
  Support for Qt Quick Designer .......... yes
  Flipable item .......................... yes
  GridView item .......................... yes
  ListView item .......................... yes
  Path support ........................... yes
  PathView item .......................... yes
  Positioner items ....................... yes
  ShaderEffect item ...................... yes
  Sprite item ............................ yes
Qt Gamepad:
  SDL2 ................................... no
Qt 3D:
  Assimp ................................. yes
  System Assimp .......................... no
  Output Qt3D Job traces ................. no
  Output Qt3D GL traces .................. no
Qt 3D GeometryLoaders:
  Autodesk FBX ........................... no
Qt Wayland Client ........................ no
Qt Wayland Compositor .................... no
Qt Bluetooth:
  BlueZ .................................. no
  BlueZ Low Energy ....................... no
  Linux Crypto API ....................... no
Qt Sensors:
  sensorfw ............................... no
Qt Quick Controls 2:
  Styles ................................. Default Material Universal
Qt Quick Templates 2:
  Hover support .......................... yes
  Multi-touch support .................... yes
Qt Positioning:
  Gypsy GPS Daemon ....................... no
  WinRT Geolocation API .................. no
Qt Location:
  Geoservice plugins:
    OpenStreetMap ........................ yes
    HERE ................................. yes
    Esri ................................. yes
    Mapbox ............................... yes
    MapboxGL ............................. no
    Itemsoverlay ......................... yes
Qt Multimedia:
  ALSA ................................... no
  GStreamer 1.0 .......................... no
  GStreamer 0.10 ......................... no
  Video for Linux ........................ yes
  OpenAL ................................. no
  PulseAudio ............................. no
  Resource Policy (libresourceqt5) ....... no
  Windows Audio Services ................. no
  DirectShow ............................. no
  Windows Media Foundation ............... no
Qt WebEngine:
  Embedded build ......................... yes
  Pepper Plugins ......................... no
  Printing and PDF ....................... no
  Proprietary Codecs ..................... no
  Spellchecker ........................... yes
  WebRTC ................................. no
  Using system ninja ..................... no
  ALSA ................................... no
  PulseAudio ............................. no
  System libraries:
    re2 .................................. no
    ICU .................................. no
    libwebp and libwebpdemux ............. no
    Opus ................................. no
    ffmpeg ............................... no

Note: Also available for Linux: linux-clang linux-icc

Note: Using static linking will disable the use of dynamically
loaded plugins. Make sure to import all needed static plugins,
or compile needed modules into the library.

Note: -optimized-tools is not useful in -release mode.

Note: QtSerialBus: Newer kernel needed for flexible data-rate frame support (canfd_frame).

Note: No wayland-egl support detected. Cross-toolkit compatibility disabled.

WARNING: Cross compiling without sysroot. Disabling pkg-config


```

`4`. 执行`make && make install`

`5`. 由于x2go 对Qt5的支持尚存在问题，QtCreater无法正常启动，因此，我们使用Eclipse 来编写第一个demo
```
wget http://mirrors.ustc.edu.cn/eclipse/technology/epp/downloads/release/2019-03/R/eclipse-cpp-2019-03-R-linux-gtk-x86_64.tar.gz
wget http://iso.mirrors.ustc.edu.cn/eclipse/tools/cdt/releases/9.7/cdt-9.7.2/cdt-9.7.2.zip
```

ps: 若wget 下载失败，请复制地址使用浏览器下载

注意eclipse 依赖jre 1.8， 需要提前准备jre，建议从pycharm中复制一个jre复制到eclipse 根目录

ps: eclipse-cpp中对Qt的支持不完整，因此需要重新安装CDT
pps: CDT对QT的支持也不完整，但是能用就OK

`6`. 使用Eclipse 新建一个Qt工程

![](assets/screenshots/2019-7-29-14-04-01.png)


<!-- 
root
NSD123dev 
 -->

### 玩转linux fb
`https://blog.csdn.net/zgrjkflmkyc/article/details/9402541`
`http://seenaburns.com/2018/04/04/writing-to-the-framebuffer/`

Qt在命令行可使用命令QT_QPA_PLATFORM=linuxfb:fb=/dev/fb1 和 -platform linuxfb使qt程序运行在该plugin上
另外指定fb用fb=/dev/fbN，分配显示区大小size=<width>x<height>，物理大小mmSize=<width>x<height>，设定便宜offset=<width>x<height>，有关于屏幕消影（blinking cursor）和闪烁光标（screen blanking）的控制nographicsmodeswitch


### linux 下虚拟显示驱动
对于没有显卡的情况，可以使用xvfb
<https://www.jianshu.com/p/df6d94a857f1>
<https://www.cnblogs.com/happyday56/p/9006629.html>


### 内核编译
首先安装依赖包：
sudo apt-get install u-boot-tools


### 查看当前系统所有的共享内存空间信息
使用`ipcs -m`可以查看当前系统所有的共享内存空间信息

### 海思相关
海思图像相关：
TDE： 1/Hi3516v300/01.software/board/MPP/TDE API参考
`1.1 概述`
> TDE（Two Dimensional Engine） 利用硬件为 OSD（On Screen Display） 和 GUI （Graphics User Interface） 提供快速的图形绘制功能， 主要有快速位图搬移、快速色彩
> 填充、快速抗闪搬移、快速位图缩放、画点、画水平/垂直线、位图格式转换、位图
> alpha 叠加、位图按位布尔运算、 ColorKey 操作



关于directfb的文档
https://doc.qt.io/archives/qt-4.8/qt-embeddedlinux-directfb.html



### 交叉编译opencv
版本3.4.7， 出现得问题参照<https://blog.csdn.net/qq_30155503/article/details/79983630>解决
ps， 可以直接直接用下面的命令而不用改CMakecache：

```bash
cmake .. -DCMAKE_CXX_FLAGS="-pthread -lrt -ldl -fpermissive -L/media/kk/data/kk/3516DV300/Qt-install/lib -lQt5MultimediaWidgets -lQt5Widgets -lQt5Multimedia -lQt5Gui -lQt5Network -lQt5Core -lQt5Test -D CV__EXCEPTION_PTR=0" -DBUILD_SHARED_LIBS=1 -DOpenCV_STATIC=1

```
### Qt qmake Makefile Example
在嵌入式linux开发中，一个很方便的办法是用qmake 组织makefile， 此时，pro例子如下：

```bash
TEMPLATE = app

QT += widgets multimediawidgets testlib
CONFIG += c++11


launch_modeall {
	CONFIG(debug, debug|release) {
	    DESTDIR = debug
	} else {
	    DESTDIR = release
	}
}

SOURCES += src/shm_yuv.cpp  src/yuv2rgb.cpp
INCLUDEPATH += ./inc /media/kk/data/kk/3516DV300/Opencv-install/include 
LIBS += -L/media/kk/data/kk/3516DV300/Opencv-install/lib -lopencv_calib3d -lopencv_imgproc -lopencv_highgui -lopencv_flann -lopencv_stitching -lopencv_imgcodecs -lopencv_videoio -lopencv_videostab -lopencv_superres -lopencv_photo -lopencv_features2d -lopencv_core -lopencv_video -lopencv_ml -lopencv_shape -lopencv_objdetect

HEADERS += inc/yuv2rgb.h
QMAKE_CFLAGS += -mcpu=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=softfp
QMAKE_CXXFLAGS += -mcpu=cortex-a7 -mfpu=neon-vfpv4 -mfloat-abi=softfp
QMAKE_LFLAGS += -L/media/kk/data/kk/3516DV300/SDK/Hi3516CV500_SDK_V2.0.1.0/smp/a7_linux/mpp/lib -lsvpruntime

# For sample_runtime
SOURCES += src/sample_runtime/common/src/*.c
SOURCES += src/sample_runtime/src/*.c
INCLUDEPATH += src/sample_runtime/common/include
INCLUDEPATH += ./src/sample_runtime/cvutils/include/ ./src/sample_runtime/include/
INCLUDEPATH += /media/kk/data/kk/3516DV300/SDK/Hi3516CV500_SDK_V2.0.1.0/smp/a7_linux/mpp/include

DEFINES += ON_BOARD
# Here only static libs can be linked, I don't know why. Please delete all shared libs in /media/kk/data/kk/3516DV300/SDK/Hi3516CV500_SDK_V2.0.1.0/smp/a7_linux/mpp/lib
LIBS +=  -lsns_imx335 -lisp -lsns_imx307 -l_hidehaze -lsns_os05a -lsvpruntime -lnnie -lmpi -lsns_imx458 -lVoiceEngine -lsns_imx307_2l -lmd -ltde -lsecurec -lhi_cipher -l_hiae -lsns_mn34220 -l_hiawb_natura -lupvqe -lsns_imx327 -l_hidrc -lsns_os05a_2l -l_hildci -live -lsns_imx377 -lsns_imx327_2l -lhdmi -ldnvqe -l_hiawb -ldl
```

相应的，对应的Makefile如下：
```makefile
PRO   = demo001.pro
QMAKE = /media/kk/data/kk/3516DV300/Qt-install/bin/qmake

all:	QtMakefile
	$(MAKE) -f QtMakefile.Debug

clean:
	rm -fr QtMakefile QtMakefile.debug QtMakefile.release debug release

QtMakefile: $(PRO)
	$(QMAKE) -o QtMakefile $(PRO) CONFIG+=debug_and_release

debug:	QtMakefile
	$(MAKE) -f QtMakefile debug

release:	QtMakefile
	$(MAKE) -f QtMakefile release

.PHONY: all clean debug clean-debug release clean-release
```

### 海思显示总结：
1. 在Qt的linuxfb的绘制主要依赖在内存中进行图片的缩放和拷贝，在TDE中有对应的函数，如果做相应的修改，则可以对Qt进行加速
2. 海思的显示架构主要分为两层，视频层和hifb管理的linuxfb设备，其中视频层的管理在文档<HiMPP V4.0 媒体处理软件开发参考>的视频输出章节，可以对视频输出的位置等信息进行设置,这部分是硬件管理的视频设备，
另外一层在3516dv300中为/dev/fb0，在LCD设置了时序等初始化工作之后，/dev/fb0才可用。 /dev/fb0主要用于UI的开发，这部分可以使用TDE进行加速。
3. hifb提供了整体的alpha混合，可以设置/dev/fb0与视频层的alpha值。

### c/cpp 混编问题
用Qt组织工程，一部分代码用c语言编写，用gcc编译，一部分语言用cpp编写，用g++编译，其中c语言的部分调用了C语言的.a，用g++链接会报符号未定义的错误

大致问题应该是gcc和g++在链接的时候使用的abi不一致，g++

### 海思nnie 开发

目标： 移植mxnet-retinaface

1. mapper 依赖protobuf, 配置时的参数如下:
`cmake -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_BUILD_SHARED_LIBS=ON ../cmake/ -DCMAKE_INSTALL_PREFIX=/media/kk/data/kk/sources/protobuf-3.5.1-install -DCMAKE_C_COMPILER=/usr/bin/gcc-4.8 -DCMAKE_C_COMPILER=/usr/bin/g++-4.8`

注意SDK中的mapper的gcc版本是 4.8， ubuntu 16带的gcc版本是5.4，版本之间有abi兼容问题。

2. 开发步骤
(1) 预处理检查：
java -jar ruyi.jar --preprocess   <net type>     <src prototxt file>            <caffemodel file>         <dest prototxt file>                  [isInplace]    
java -jar ruyi.jar --preprocess   0              bvlc_alexnet_deploy.prototxt   bvlc_alexnet.caffemodel   bvlc_alexnet_deploy_output.prototxt  true
java -jar ruyi.jar -p             <net type>     <src prototxt file>            <caffemodel file>           [isInplace]
java -jar ruyi.jar -p             0              bvlc_alexnet_deploy.prototxt   bvlc_alexnet.caffemodel   bvlc_alexnet_deploy_output.prototxt  true
主要目的是探测网络中有没有不支持的层。

PS:  windows的ruyistudio有一整套的mapper， 不用安装。
(2) 

