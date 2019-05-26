```bash
找一台可以联网的ubuntu电脑， 可以是WSL，不要求版本
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


# sudo apt update && sudo apt install linux-generic
# grub-pc

寻找根文件分区的 UUID:
ls -l /dev/disk/by-uuid/ |grep sda3

cat >  /etc/fstab << "EOF"
proc /proc proc defaults 0 0
UUID=d8b27c84-b572-46ab-a75f-273c42fe70ec / ext4 defaults,errors=remount-ro,relatime 0 1
EOF

dpkg-reconfigure locales
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

安装自己喜欢的桌面
sudo apt install ubuntu-desktop
suodo apt install gnome-core xorg

```
