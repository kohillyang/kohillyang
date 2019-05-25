```bash
sudo apt update
sudo apt install debootstrap
sudo mount /dev/sda3 rootfs
sudo debootstrap --verbose --arch=amd64 xenial rootfs/ http://mirrors.aliyun.com/ubuntu


sudo mount -o bind /dev ./rootfs/dev
sudo mount -o bind /sys ./rootfs/sys
sudo mount -t proc proc ./rootfs/proc
sudo chroot rootfs/
adduser ubuntu
sudo dpkg-reconfigure locales
sudo dpkg-reconfigure console-setup
sudo apt update && sudo apt install linux-generic grub-pc

寻找根文件分区的 UUID:
ls -l /dev/disk/by-uuid/ |grep sda3

cat >  /etc/fstab << "EOF"
proc /proc proc defaults 0 0
UUID=d8b27c84-b572-46ab-a75f-273c42fe70ec / ext4 defaults,errors=remount-ro,relatime 0 1
EOF


dpkg-reconfigure locales
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
sudo apt install ubuntu-desktop


```
