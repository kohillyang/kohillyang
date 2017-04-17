---
layout: post
title: How to boot Openwrt kernel By Uefi.
date: 2017-01-09 15:46
comments: true
external-url:
categories: linux
---

### How to boot EFI kernel using QEMU (kvm)?

1. <http://unix.stackexchange.com/questions/52996/how-to-boot-efi-kernel-using-qemu-kvm>
2. <https://github.com/tianocore/tianocore.github.io/wiki/How-to-run-OVMF>

其中[2]是QEMU的UEFI固件，注意32位的UEFI固件启动的是/EFI/Boot/bootia32.efi,64位UEFI固件启动的是/EFI/Boot/bootx64.efi，用该BIOS固件启动KVM的命令如下：

```bash
sudo kvm  --bios  ./OVMF.fd /dev/sdb -net nic,model=ne2k_pci -net user -soundhw es1370 -serial stdio
sudo kvm  --bios  ./OVMF.fd /dev/loop0  -serial stdio
```
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


