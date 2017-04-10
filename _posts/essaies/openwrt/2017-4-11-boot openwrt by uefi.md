---
layout: post
title: How to boot Openwrt kernel By Uefi.
date: 2017-01-09 15:46
comments: true
external-url:
categories: OpenWrt
---

### How to boot EFI kernel using QEMU (kvm)?

1. <http://unix.stackexchange.com/questions/52996/how-to-boot-efi-kernel-using-qemu-kvm>
2. <https://github.com/tianocore/tianocore.github.io/wiki/How-to-run-OVMF>

其中[2]是QEMU的UEFI固件

```bash
sudo kvm  --bios  ./OVMF.fd /dev/sdb --net none -serial stdio
```

### How to boot Openwrt using uefi?

本文中的启动盘来源于<http://bbs.wuyou.net/forum.php?mod=viewthread&tid=310626>，关于启动盘的制作可参考
1. <https://www.douban.com/note/210077866/?type=like>
2. <http://bbs.wuyou.net/forum.php?mod=viewthread&tid=310626>
3. <http://bbs.wuyou.net/forum.php?mod=viewthread&tid=339411&extra=page%3D1>
这里就不说了

基础知识：
1. uefi启动分区只能是fat,fat32，linux下新建的默认为fat，即fat16，因此uefi的启动文件必须放在fat分区。
2. openwrt为linux内核，一般使用linux引导，因此启动顺序为：uefi-grub2-linux内核。
3. linux内核即boot分区下的/boot/vmlinuz，或者编译出来的xxx-linuz，这是一个压缩的内核,在启动的过程中会有一个自解压的过程。
4. 内核启动过程中，会提供一个/挂载点，随后可以挂载你自己的root到/挂载点。我们常用的chroot就是切换挂载点/的过程。

openwrt分区
根据编译出来的img文件，默认会有两个ext4（也可能是其他格式的）分区，第一个分区为boot分区，默认不是fat格式，我们需要把它里面的文件提取出来，然后把第一个分区格式化为fat格式，然后把复制出来的文件再复制回去。
第二个分区即rootfs，这个分区的位置在grub.cfg中由UUID指定

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