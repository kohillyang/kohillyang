---
layout: post
title: Linux
date: 2017-02-13 19:40
comments: true
external-url:
categories: linux 
permalink: /notes_linux
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