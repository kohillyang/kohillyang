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