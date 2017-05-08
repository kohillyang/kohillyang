---
layout: post
title: How to boot Openwrt kernel By Uefi.
date: 2017-01-09 15:46
comments: true
external-url:
categories: linux
---
<br>

### 关于kvm

```bash
kohill@ubuntu:/usr/bin$ ls *qemu*
qemu-img  qemu-nbd          qemu-system-x86_64
qemu-io   qemu-system-i386  qemu-system-x86_64-spice
```

kvm 目测是qemu-system-x86_64的符号链接，因为感觉功能是一样的，参数也通用。

<https://gmplib.org/~tege/qemu.html>

### How to boot EFI kernel using QEMU (kvm)?

1. <http://unix.stackexchange.com/questions/52996/how-to-boot-efi-kernel-using-qemu-kvm>
2. <https://github.com/tianocore/tianocore.github.io/wiki/How-to-run-OVMF>

其中[2]是QEMU的UEFI固件，注意32位的UEFI固件启动的是/EFI/Boot/bootia32.efi,64位UEFI固件启动的是/EFI/Boot/bootx64.efi，用该BIOS固件启动KVM的命令如下：

```bash
sudo kvm  --bios  ./OVMF.fd /dev/sdb -net nic,model=ne2k_pci -net user -soundhw es1370 -serial stdio
sudo kvm  --bios  ./OVMF.fd /dev/loop0  -serial stdio
```
如果在编译的时候集成了virtio gpu driver, 可以试试下面的启动命令：

```bash
sudo kvm  --bios ./OVMF.fd  -serial stdio --set device.video0.driver=virtio-vga --display gtk,gl=on new.img
```

网卡参考<http://www.tuicool.com/articles/i63Ivy>

[OVME点我下载]({{ site.github_cdn_prefix }}/OVMF-X64-r15214.zip)

### How to boot Openwrt using uefi?

本文中的启动盘来源于<http://bbs.wuyou.net/forum.php?mod=viewthread&tid=310626>，关于启动盘的制作可参考
1. <https://www.douban.com/note/210077866/?type=like>
2. <http://bbs.wuyou.net/forum.php?mod=viewthread&tid=310626>
3. <http://bbs.wuyou.net/forum.php?mod=viewthread&tid=339411&extra=page%3D1>

### 启动盘制作命令：

从<http://alpha.gnu.org/gnu/grub/grub-2.02~rc1-for-windows.zip>下载grub2并解压，切换到解压后的目录，执行以下命令

```bash
grub-mkimage.exe -d i386-efi  -p /EFI/Boot/ -o bootia32.efi -O  i386-efi part_gpt part_msdos disk fat exfat ext2 ntfs appleldr hfs iso9660 normal search_fs_file 
```
-p 是指定grub的前缀，相当于指定配置文件的目录，启动如果没有找到这个目录，那么会进入grub2命令行。ls命令可以查看分区啥的。

命令会在当前目录下生成bootia32.efi文件，改名后复制到/EFI/Boot/下就行了。32位的UEFI固件启动的是/EFI/Boot/bootia32.efi,64位UEFI固件启动的是/EFI/Boot/bootx64.efi。然后可在/EFI/Boot/下新建一个Grub.cfg，里面可以创建菜单，加载字体，替换背景之类。


```bash
set pager=1
insmod all_video
insmod video_bochs
insmod video_cirrus
insmod efi_gop
insmod efi_uga
insmod font
insmod gfxterm
insmod gfxmenu
insmod gettext
insmod jpeg
insmod ext2
#加载unicode字体显示中文
loadfont /neyan/grub2_efi/fonts/unicode.pf2
set locale_dir=/neyan/grub2_efi/locale
set lang=zh_CN
#设置分辨率
set gfxmode=auto
terminal_output gfxterm
background_image /neyan/grub2_efi/back.jpg
#倒计时
set timeout=3
#颜色
set color_normal=green/black
set color_highlight=white/cyan
menuentry "OpenWrt" {
set root='(hd0,msdos1)'
linux /boot/vmlinuz root=PARTUUID=cacf3a9c-02 rootfstype=ext2 rootwait intel_idle.max_cstate=1 console=tty0 console=ttyS0,38400n8 noinitrd
}
menuentry "OpenWrt (failsafe)" {
	linux /boot/vmlinuz failsafe=true root=PARTUUID=cacf3a9c-02 rootfstype=ext2 rootwait intel_idle.max_cstate=1 console=tty0 console=ttyS0,38400n8 noinitrd
}

menuentry "启动EFI SHELL" {
echo "正在启动EFI SHELL，请等待...."
search --file /rdtobot/efi_file/boot/bootx64.efi --set=root
chainloader ($root)/rdtobot/efi_file/boot/bootx64.efi
}

menuentry "启动 MHDD" {
set root='(hd0,msdos1)'
linux /boot/vmlinuz
search --file /op.img --set=root
initrd  /op.img 
}
menuentry "重启"{
reboot
}
menuentry "关机"{
halt
}
```
自动挂载openwrtimg的脚本

```bash
mount:
    losetup -fP new.img
    mount -rw /dev/loop0p1 boot
    mount -rw /dev/loop0p2 root
del:
    -umount boot
    -umount root
    -losetup -d /dev/loop0
kvm:
    kvm new.img --serial stdio 
kvm-uefi:
    kvm --bios OVMF.fd --serial stdio new.img 
#--device virtio-gpu-pci 

vmdk:
    qemu-img convert -f raw new.img -O vmdk new.vmdk 
grub:
    losetup -fP new.img
    ls /dev/loop0*
    mount /dev/loop0p1 /mnt
    echo "(hd0) /dev/loop0" > loop0device.map 
    grub-install --no-floppy --grub-mkdevicemap=loop0device.map --modules="part_msdos" --boot-directory=/mnt /dev/loop0 -v
    umount /mnt
    losetup -d /dev/loop0
kvm-nograph:
    kvm new.img -net nic -net tap,ifname=vnet0,script=scripts/ifup.sh,downscript=script/ifdown.sh --serial stdio
#-nographic


.PHONY : del mount
```

### 关于grub2的详细教程
请参阅<https://docs.google.com/document/d/1O9K0ZmrqPW4FuGMJ1s2fmpCmV8NR_BWD0PrNw3uopr8/preview>(需翻墙)



### KVM如何以桥接方式联网
首先是启动参数
<pre>kvm new.img -net nic -net tap,ifname=vnet0,script=scripts/ifup.sh,downscript=script/ifdown.sh --serial stdio</pre>
其中script指定了kvm 启动时要执行的脚本

```bash
#!/bin/bash
#
ifconfig br0 down
bridge=br0
brctl delbr br0
brctl addbr br0 
if [ -n "$1" ]; then
        echo $*
        ip link set $1 up
        sleep 1
        brctl addif $bridge $1
        brctl addif br0 ens38
#       brctl addif br0 ens40
        ifconfig br0 up
#       ip addr add 192.168.4.100 dev br0
#       ip addr add 192.168.4.133 dev $1
else
        echo "Error: no interfacespecified."
        exit 1
```
大概就是先创建一个网桥，然后把$1和宿主机中的网卡桥接起来。

PS: 如果宿主机本身也是桥接方式联网，那么宿主机和kvm启动的虚拟机都可以自动从路由器dhcp获取地址。