```bash
找一台可以联网的ubuntu电脑， 可以是WSL，不要求版本，livecd我这边测试失败，因此不建议livecd, 无论是在WSL上还是在原生linux，建议在home下执行下面的命令，不建议在/mnt下执行下面的命令，所有的命令需要sudo，并且需要分区具有可执行权限（注意是分区而不是文件）。
sudo apt update
sudo apt install debootstrap
mkdir rootfs
# sudo mount /dev/sda3 rootfs
sudo debootstrap --verbose --arch=amd64 xenial rootfs/ https://mirrors.tuna.tsinghua.edu.cn/ubuntu/
sudo mount -o bind /dev ./rootfs/dev
sudo mount -o bind /sys ./rootfs/sys
sudo mount -t proc proc ./rootfs/proc
sudo chroot rootfs/


下面的命令在chroot环境中执行, 注意不要在screen命令中执行，可以在ssh中执行
mount -t devpts devpts /dev/pts
sudo apt install nano
adduser ubuntu
sudo locale-gen en_US en_US.UTF-8
sudo dpkg-reconfigure locales
sudo dpkg-reconfigure console-setup

下面的命令会弹出grub的安装菜单，建议选择跳过安装grub。
sudo apt update && sudo apt install linux-generic
# grub-pc

寻找根文件分区的 UUID:
ls -l /dev/disk/by-uuid/ |grep sda3


cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

安装自己喜欢的桌面
sudo apt install ubuntu-desktop
sudo apt install gnome-core xorg
umount /dev/pts
sudo apt clean
exit

umount rootfs/dev
umount rootfs/proc
umount rootfs/sys

退出chroot环境之后，将rootfs打包，然后用livecd启动，然后在给定分区解包
下面最难的一部分：引导该系统
```
