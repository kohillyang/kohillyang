---
layout: post
title: notes of openwrt
date: 2017-02-13 19:40
comments: true
external-url:
categories: OpenWrt 
permalink: /notes_openwrt
---
<br>

　　本文只是笔记，所述内容仅供参考，大部分未经测试。

### OpenWrt获取源码（已测试）
　　[访问https://dev.openwrt.org/wiki/GetSource](https://dev.openwrt.org/wiki/GetSource)。

```bash
sudo apt-get install gawk  libssh-dev  gcc g++ binutils patch bzip2 flex bison make autoconf gettext texinfo unzip sharutils subversion libncurses5-dev ncurses-term zlib1g-dev libperl-dev file libp11-kit-dev
./scripts/feeds update -a
./scripts/feeds install -a
```

### 列出所有监听的端口（已测试）
`netstat -nlp | grep LISTEN` <br>
netstat命令各个参数说明如下：<br>
　　-t : 指明显示TCP端口<br>
　　-u : 指明显示UDP端口<br>
　　-l : 仅显示监听套接字(所谓套接字就是使应用程序能够读写与收发通讯协议(protocol)与资料的程序)<br>
　　-p : 显示进程标识符和程序名称，每一个套接字/端口都属于一个程序。<br>
　　-n : 不进行DNS轮询(可以加速操作)<br>
　　比如，要显示所有的TCP连接，所用命令为：`netstat -ntp`<br>

### 防火墙设置（除另外指明外，均没有测试）
　　openwrt下的防火墙原理是通过uci解码产生iptables规则，所以下面的配置文件都有等效的iptable命令。<br>
　　查看iptables已启用策略:<code>iptables -L</code>

```bash
#DMZ主机
config redirect
        option target 'DNAT'
        option src 'wan'
        option dest 'lan'
        option proto 'tcp udp'
        option src_dport '1-65535'
        option dest_ip '192.168.2.252'
        option dest_port '1-65535'
        option name 'Forward'
#拦截指定MAC地址
config rule
        option src              'lan'
        option dest             'wan'
        option src_mac          '00:00:00:00:00'
        option target           'REJECT'
#拦截局域网到 123.45.67.89的访问请求
config rule
        option src              'lan'
        option dest             'wan'
        option dest_ip          '123.45.67.89'
        option target           'REJECT'
#重定向：局域网访问10.55.34.85的请求将被重定向到63.240.161.99的123端口,可以用来做网页重定向
config redirect
        option src              'lan'
        option dest             'wan'
        option src_ip           '10.55.34.85'
        option src_dip          '63.240.161.99'
        option dest_port        '123'
        option target           'SNAT'
#端口映射：来自internet的使用tcp协议访问路由80端口的请求映射到内网192.168.1.10的 80端口,可以映射端口提高P2P效率
config redirect
        option src 'wan'
        option src_dport '80'
        option proto 'tcp'
        option dest_ip '192.168.1.10'
## 允许来自wan的发往51413的连接
config rule
        option name 'transmission'
        option src 'wan'
        option proto 'tcp udp'
        option dest_port '51413'
        option family 'ipv6'
        option target 'ACCEPT'
        option dest 'lan'
## 允许来自wan的发往51413的连接
config rule 'transmission_peer_tcp'
        option src 'wan'
        option dest_port '51413'
        option proto 'tcp udp'
        option target 'ACCEPT'
        option name 'transmission_web_ipv4'

```

### 允许IPV6&IPV4某个端口的访问请求(测试成功)

运行在路由器上的程序已经监听了某个端口但是外网依旧无法访问时，可以尝试下面的命令：

`iptables -I INPUT -p tcp --dport PORT_NUMBER -j ACCEPT`

同样对于IPV6，命令如下
`ip6tables -I INPUT -p tcp --dport PORT_NUMBER -j ACCEPT`

### Example：利用iptables记录日志(未成功)

```
iptables -A INPUT -i wan+ -p tcp --dport 51413 -j LOG --log-prefix "iptables_51413_tcp_alert" --log-level debug
iptables -A INPUT -i wan+ -p udp --dport 51413 -j LOG --log-prefix "iptables_51413_udp_alert" --log-level debug
ip6tables -A INPUT -i wan+ -p tcp --dport 51413 -j LOG --log-prefix "ip6tables_51413_tcp_alert" --log-level debug
ip6tables -A INPUT -i wan+ -p udp --dport 51413 -j LOG --log-prefix "ip6tables_51413_udp_alert" --log-level debug
```

### 重启防火墙(测试成功)
`/etc/init.d/firewall restart`

### 利用curl获取IP(测试成功)

```
#get IPv4 address
echo `curl -4 -s icanhazip.com`
#get IPV6 address
echo `curl -6 -s icanhazip.com`
```

### 利用iptables实现port forwarding(测试成功)
开启端口转发功能，编辑/etc/sysctl.conf，使net.ipv4.ip_forward=1，随后`sysctl -p`。

```bash
wan_addr=`curl -4 -s icanhazip.com`
dest_port_wan=6800
dest_port_lan=6800
dest_addr_lan=192.168.1.1

#add forwarding rule
iptables -t nat -A PREROUTING  -p tcp -m tcp -d $wan_addr --dport     $dest_port_wan -j DNAT --to-destination $dest_addr_lan:$dest_port_lan
iptables -A FORWARD -m state -p tcp -d $dest_addr_lan --dport     $dest_port_lan --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -p tcp -m tcp -s $dest_addr_lan --sport $dest_port_lan -j SNAT --to-source $wan_addr

#remove forwarding rule
iptables -t nat -D PREROUTING  -p tcp -m tcp -d $wan_addr --dport     $dest_port_wan -j DNAT --to-destination $dest_addr_lan:$dest_port_lan
iptables -D FORWARD -m state -p tcp -d $dest_addr_lan --dport     $dest_port_lan --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -D POSTROUTING -p tcp -m tcp -s $dest_addr_lan --sport     $dest_port_lan -j SNAT --to-source $wan_addr
```

### 关于iptable的一个性能问题(blocking packets it shouldn't be)
[Why is UFW/iptables blocking packets it shouldn't be?](http://www.linuxquestions.org/questions/linux-networking-3/why-is-ufw-iptables-blocking-packets-it-shouldn%27t-be-4175500239/)

### 删除LUCI缓存（已测试）
rm /tmp/luci-indexcache

### 安装支持IPv6的http代理(已测试)

```bash
opkg update
opkg install tinyproxy luci-app-tinyproxy
uci set tinyproxy.@tinyproxy[0].enabled=1
uci commit
/etc/init.d/tinyproxy enable
/etc/init.d/tinyproxy restart
rm /tmp/luci-indexcache
```
参考配置文件：

```bash
config tinyproxy
        option Port '8888'
        option Timeout '600'
        option DefaultErrorFile '/usr/share/tinyproxy/default.html'
        option StatFile '/usr/share/tinyproxy/stats.html'
        option MaxClients '100'
        option MinSpareServers '5'
        option MaxSpareServers '20'
        option StartServers '10'
        option MaxRequestsPerChild '0'
        option ViaProxyName 'tinyproxy'
        option enabled '1'
        option User 'root'
        option Listen '0.0.0.0'
        option Syslog '1'
        option Group 'nogroup'
        list Allow '::ffff:0:0/96'
        list ConnectPort '0'
        list ConnectPort 443
        list ConnectPort 563
```

### 利用ip6tables 设置NAT6(已测试)
注意ula_prefix不能以f开头

```bash
LAN_ULA_PREFIX=$(uci get network.globals.ula_prefix)
WAN6_INTERFACE='pppoe-wan'
WAN6_GATEWAY=$(route -A inet6 -e | grep "pppoe-wan" | awk '/::\/0/{print $2; exit}')
ip6tables -t nat -I POSTROUTING -s "$LAN_ULA_PREFIX" -o "$WAN6_INTERFACE" -j MASQUERADE
route -A inet6 add 2000::/3 gw "$WAN6_GATEWAY" dev "$WAN6_INTERFACE"
```

### 同时支持IPV4与IPV6端口扫描的网站(已测试)
<http://www.ipv6scanner.com>

### 配置多拨(已测试)
执行`opkg update && opkg install kmod-macvlan`之后，执行`ip link add link eth1 type macvlan`，这会生成一个名字为macvlan0,mac随机的虚拟网卡，以此为物理网卡在interface下新建一个pppoe连接，记下你的接口名(pppoe-wan开头，比如pppoe-wan2)，执行下面的代码手动拨号（不是百分百成功，隔一段时间试几次），注意替换pppoe-wan2，$usrname，$passwd。

```bash
/usr/sbin/pppd nodetach ipparam wan ifname pppoe-wan2 +ipv6 set AUTOIPV6=1 nodefaultroute usepeerdns maxfail 1 user $usrname password $passwd ip-up-script /lib/netifd/ppp-up ipv6-up-script /lib/netifd/ppp-up ip-down-script /lib/netifd/ppp-down ipv6-down-script /lib/netifd/ppp-down mtu 1492 mru 1492 plugin rp-pppoe.so nic-macvlan0
```
<img src="{{ site.github_cdn_prefix }}/screenshots/2017-3-1 0000.jpg" class="img-responssive">

### 在DDWRT上安装opkg(已测试)
<http://www.right.com.cn/forum/thread-201603-1-1.html>

ddwrt官方论坛上的一个讨论<http://www.dd-wrt.com/phpBB2/viewtopic.php?p=904874>

自己研究出的一个解决方法：
<ol>
<li>复制整个系统（etc,lib,sbin,usr,opt,bin）到ext3分区（官方固件不原生支持ext4）</li>
<li>执行以下命令:</li>
<pre>
mkdir /jffs/rootfs
cp -a /bin /lib /sbin /usr /opt /etc /jffs/rootfs/
mount --bind /jffs/rootfs/bin /bin
mount --bind /jffs/rootfs/lib /lib
mount --bind /jffs/rootfs/sbin /sbin
mount --bind /jffs/rootfs/usr /usr
mount --bind /jffs/rootfs/opt /opt
mount --bind /jffs/rootfs/etc /etc
</pre>
启动脚本：
<pre>
mount --bind /jffs/rootfs/bin /bin
mount --bind /jffs/rootfs/lib /lib
mount --bind /jffs/rootfs/sbin /sbin
mount --bind /jffs/rootfs/usr /usr
mount --bind /jffs/rootfs/opt /opt
mount --bind /jffs/rootfs/etc /etc
sleep 1
aria2c --conf-path=/jffs/etc/aria2.conf -D
</pre>

<li>下载上文链接中的libc.ipk以及opkg.ipk，用tar解压到jffs目录。</li>

Note: DDWRT内核版本号很低，所以基本所有kmod开头的包都不能用，但本人测试aria2还是能装上的(官方包安装上之后不能用，但是可以用我自己编译的Aria2 1.31.0)。

<li>更改/etc/opkg.conf，为下面的内容，注意要根据你自己的cpu版本更改，我的CPU是AR71xx。
不建议使用12.09的内容，里面的包版本太老。</li></ol>

```bash
dest root /
dest ram /tmp
lists_dir ext /var/opkg-lists
option overlay_root /overlay
src/gz barrier_breaker_base http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/base
src/gz barrier_breaker_luci http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/luci
src/gz barrier_breaker_packages http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/packages
src/gz barrier_breaker_routing http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/routing
src/gz barrier_breaker_telephony http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/telephony
src/gz barrier_breaker_management http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/management
src/gz barrier_breaker_oldpackages http://downloads.openwrt.org/barrier_breaker/14.07/ar71xx/generic/packages/oldpackages
option force_space
```

### ubuntu安装openvpn
<http://www.linuxidc.com/Linux/2014-08/105925.htm>

### 配置stunnel
`openssl req -new -x509 -days 3650 -nodes -out stunnel.pem -keyout stunnel.pem`
`openssl gendh 512>> stunnel.pem  `

### DDWRT设置IPV6（未成功）

```bash
WAN6_INTERFACE='ppp0'
WAN6_GATEWAY=$(route -A inet6 -e | grep "pppoe-wan" | awk '/::\/0/{print $2; exit}')
ip -6 route add 2001:250:1001:2500:2037:f4d:1dc8:e7c8/128 dev br0 metric 128
ip -6 neigh add proxy 2001:250:1001:2500:2037:f4d:1dc8:e7c8 dev vlan1
route -A inet6 add 2000::/3 gw "$WAN6_GATEWAY" dev "$WAN6_INTERFACE"
route -A inet6 add 2001:250:1001:2500:2037:f4d:1dc8:e7c8/128 gw fe80::224:1ff:fee7:85b6 dev br0
```

### DDWRT上加载ip6tables NAT模块
<http://blog.jmwhite.co.uk/2013/08/10/ipv6-tunnels-on-dd-wrt-with-3-x-kernel-builds/>
`dmesg`会显示模块加载时有哪些错误。

### openwrt官方关于无线的支持信息
包括无线网卡支持列表等。
<https://wiki.openwrt.org/doc/howto/wireless.overview#>


### X86编译


<li>镜像生成器</li>

如果没有什么特殊要求，可以直接用镜像生成器直接打包，方便快捷，几分钟生成一个镜像包。

<http://wiki.openwrt.org/zh-cn/doc/howto/imagebuilder>

镜像生成器下载

<http://downloads.openwrt.org/backfire/10.03.1-rc6/x86_generic/OpenWrt-ImageBuilder-x86-for-Linux-i686.tar.bz2>


<li> x86肯定是需要打开USB支持的（已测试）</li>

```bash
Make kernel_menuconfig
Device Drivers  --->
  SCSI device support  --->
(Although SCSI will be enabled automatically when selecting USB Mass Storage,
we need to enable disk support.)
---   SCSI support type (disk, tape, CD-ROM)
<*>   SCSI disk support
(Then move back a level and go into USB support)
USB support  --->
(This is the root hub and is required for USB support.
If you'd like to compile this as a module, it will be called usbcore.)
<*> Support for Host-side USB
(Select at least one of the HCDs. If you are unsure, picking all is fine.)
--- USB Host Controller Drivers
<*> EHCI HCD (USB 2.0) support
< > OHCI HCD support
<*> UHCI HCD (most Intel and VIA) support
(Moving a little further down, we come to CDC and mass storage.)
< > USB Modem (CDC ACM) support
<*> USB Printer support
<*> USB Mass Storage support
(If you have a USB Network Card like the RTL8150, you'll need this)
USB Network Adapters  --->
    <*> USB RTL8150 based ethernet device support (EXPERIMENTAL)
(If you have a serial to USB converter like the Prolific 2303, you\'ll need this)
USB Serial Converter support  --->
    <*> USB Serial Converter support
    <*> USB Prolific 2303 Single Port Serial Driver (NEW)
```

<li> 开启4G内存支持</li>
如果没有找到，在界内核配置界面搜索high能找到的

```bash
make kernel_menuconfig
  kernel configuration
     Processor type and features

      <*> high memory support
```

<li> 增加温度传感器</li>
*  替换/dd/feeds/luci/modules/luci-mod-admin-full/luasrc/view/admin_status/index.htm
*  在menuconfig里添加Utilities/lm-sensors-detect
*  在kernel_menuconfig里

```bash
Device Drivers/I2C support
GPIO Support
Hardware Monitoring support 3个选项
```
选自己硬件
*  我在Hardware Monitoring support把所有的选项都勾上了，并且勾上了I2C support。
admin_status/index.htm 中加入

```html
<tr><td width="33%"><%:Core0 Temperature%></td><td><%=luci.sys.exec("cut -c1-2 /sys/class/hwmon/hwmon0/temp2_input")%></td></tr>
<tr><td width="33%"><%:Core2 Temperature%></td><td><%=luci.sys.exec("cut -c1-2 /sys/class/hwmon/hwmon0/temp4_input")%></td></tr>
<tr><td width="33%"><%:Core0 scaling_governor%></td><td><%=luci.sys.exec("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")%></td></tr>
<tr><td width="33%"><%:Core2 scaling_governor%></td><td><%=luci.sys.exec("cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor")%></td></tr>
<tr><td width="33%"><%:Core0 scaling_governor%></td><td><%=luci.sys.exec("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")%></td></tr>
<tr><td width="33%"><%:Core2 scaling_governor%></td><td><%=luci.sys.exec("cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq")%></td></tr>
```
查看温度命令：

```bash
#!/bin/sh

CPU_TEMP=`cut -c1-2 /sys/class/hwmon/hwmon2/temp1_input`
DDR_TEMP=`cut -c1-2 /sys/class/hwmon/hwmon1/temp1_input`
WIFI_TEMP=`cut -c1-2 /sys/class/hwmon/hwmon1/temp2_input`

echo "CPU" $CPU_TEMP
echo "DDR" $DDR_TEMP
echo "WIFI" $WIFI_TEMP
```

<li> 失效的源</li>
aircrack-ng

snort需要能连接上谷歌（libdnet）

```bash
libdnet provides a simplified, portable interface to several low-level networking routines, including
network address manipulation
kernel arp(4) cache and route(4) table lookup and manipulation
network firewalling (IP filter, ipfw, ipchains, pf, PktFilter, ...)
network interface lookup and manipulation
IP tunnelling (BSD/Linux tun, Universal TUN/TAP device)
raw IP packet and Ethernet frame transmission
```

<li> 开启多核心支持</li>
```bash
Processor type and features  --->     [*] Symmetric multi-processing support
    Processor family (Core 2/newer Xeon)  --->#自行选择处理器平台     [*] Supported processor vendors  --->#自行选择处理器平台     (2) Maximum number of CPUs #自行编辑
    [*] SMT (Hyperthreading) scheduler support#超线程支持
    [*] Multi-core scheduler support
    High Memory Support (4GB)  --->
```

<li> 无线支持</li>
NetWork下选中wireless下的hostapd以及hostapd-utils，wirelss下的horsrt

到kernel-drivers里选中无线驱动

<li> NAT支持</li>
在kernel-modules下选中所有的netfilter externsions

<li>加入luci-app-aria2</li>
参见<https://github.com/nanpuyue/openwrt-extra>

<li>luci-app-vsftpd</li>
参见<https://github.com/animefansxj/luci-app-vsftpd/tree/master/Ipk>

<li>luci-app-smartinfo</li>
参见<https://github.com/animefansxj/luci-app-smartinfo>

<li>出现文件系统只读的解决办法（我似乎没有找到hotplug？）</li>
出错原因：出现这个问题的原因是编译的固件里少了hotplug

解决方案：make menuconfig -> Base system -> hotplug2要选择上

>描述：udev 是Linux kernel 2.6系列的设备管理器。它主要的功能是管理/dev目录底下的设备节点。Hotplug2是一个UDev的某些非关键功能的替代模块，为Linux早期的用户空间服务，主要负责RAM初始化和FS初始化。

其实我建议根文件系统还是只读，在上面增加一个overlay，这样在系统因为设置原因无法启动时，只需格式化或者清空overlay即可，而不需要重新烧写固件。

<li>添加openssh-sftp-server</li>
<li>添加openssl-utils（用于使用openssl生成证书）</li>

### 自编译镜像下载
[点我下载]({{ site.github_cdn_prefix }}/openwrt/x86/openwrt-x86-generic-combined-ext4.zip)
<li>最大支持2G内存，最大支持8核心</li>
<li>集成常见wifi驱动</li>
<li>集成aria2,vsftpd,nat6等常见软件</li>
<li>驱动为intel_pstate</li>
查看可用节能策略：

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
```
设置节能策略：

```bash
for f in /sys/devices/system/cpu/*/cpufreq/scaling_governor; do
echo "powersave" > $f;
done
```



### Shadowsocks Server安装
参见<http://blog.csdn.net/hanshileiai/article/details/49302865>


### 在路由器上装debian
参见<https://wiki.debian.org/InstallingDebianOn/D-Link/DIR-825>
<https://routeragency.com/?p=396>

### openwrt上设置强制40MHZ

```bash
uci set wireless.@wifi-device[0].htmode=HT40-
uci set wireless.@wifi-device[0].noscan=1
uci commit
/etc/init.d/network restart
```

编译到固件的方法：

来源<http://www.right.com.cn/forum/thread-178031-1-1.html>

```bash
直接上修改方法：
1.修改base.po添加中文支持
feeds/luci/modules/luci-base/po/zh-cn/base.po
添加
msgid "Force 40MHz mode"
msgstr "强制40MHz频宽"

msgid ""
"Always use 40MHz channels even if the secondary channel overlaps. Using this "
"option does not comply with IEEE 802.11n-2009!"
msgstr "强制启用40MHz频宽并忽略辅助信道重叠。此选项不兼容IEEE 802.11n-2009!"

2.修改wifi.lua添加设置
feeds/luci/modules/luci-mod-admin-full/luasrc/model/cbi/admin_network/wifi.lua
在------------------- MAC80211 Device ------------------上面两个 end中间添加代码（红色部份）


                m:set(section, "channel", value[2])
                 m:set(section, "htmode", value[3])
end
        noscan = s:taboption("general", Flag, "noscan", translate("Force 40MHz mode"),
        translate("Always use 40MHz channels even if the secondary channel overlaps. Using this option does not comply with IEEE 802.11n-2009!"))
        noscan.default = noscan.disabled
end

------------------- MAC80211 Device ------------------

3.改完后再编译固件
```

### MiniDLNA（已测试）

一台电脑连接到RT-N66U，然后刷成OpenWRT固件，并设置Internet连线，确保可以正常访问Internet。

电脑端cmd -> telnet192.168.1.1连接到路由器，执行以下命令：

```bash
root@OpenWrt:~# opkg update
root@OpenWrt:~# opkg install minidlna
root@OpenWrt:~# opkg install luci-app-minidlna
```

### 配置Shadowsockes
Openwrt上配置Shadowsockes server
1. <http://ntgeralt.blogspot.com/2015/12/openwrtshadowsocks.html>
2. <http://www.right.com.cn/forum/forum.php?mod=viewthread&tid=180666>
3. <http://blog.csdn.net/hanshileiai/article/details/49302865>
4. <https://github.com/shadowsocks/luci-app-shadowsocks>
5. <https://github.com/shadowsocks/openwrt-shadowsocks/blob/master/Makefile#L51>

### luci-theme-material（已测试）
<https://github.com/LuttyYang/luci-theme-material/releases>

### openwrt上安装debian（已测试）
<http://www.right.com.cn/FORUM/thread-101737-1-1.html>

<http://www.linuxquestions.org/questions/debian-26/how-to-install-debian-using-debootstrap-4175465295/>

```bash
debootstrap --include locales --arch i386 wheezy /root/debian https://mirrors.xjtu.edu.cn/debian/
cp /etc/mtab /root/debian/etc/mtab #It keeps the df command happy.
mount -o bind /dev /root/debian/dev
mount -o bind /proc /root/debian/proc
#mount -o bind /sys /root/debian/sys
chroot /root/debian/ /bin/bash
```

after chroot:

```bash
# /debootstrap/debootstrap --second-stage
echo "kohill-router" > /etc/hostname
dpkg-reconfigure locales
passwd
adduser kohill
apt-get update
apt-get install sudo syslog-ng

chmod u+w /etc/sudoers
echo '
kohill            ALL=(ALL)                ALL
' >> /etc/sudoers
chmod u-w /etc/sudoers

login

```

之后重启再进入时，只需执行下面的命令即可

```bash
mount -o bind /dev /root/debian/dev
mount -o bind /proc /root/debian/proc
#mount -o bind /sys /root/debian/sys
chroot /root/debian/ /bin/bash
```

添加启动项：

```bash
echo '#!/bin/sh /etc/rc.common
START=57
boot(){
    mount -o bind /dev /root/debian/dev
    mount -o bind /proc /root/debian/proc
}
start(){
    boot
}
stop(){
    umount /root/debian/dev
    umount /root/debian/proc
}' > /etc/init.d/debian_init
chmod +x /etc/init.d/debian_init
/etc/init.d/debian_init enable
```

如果遇到`must be a terminal`之类的错误

```bash
mount -t devpts devpts /dev/pts
```

### 配置电源键
input modules -> ACHI BUTTONS


### 配置pptpd vpn

```
opkg install kmod-gre kmod-ipt-conntrack-extra kmod-ipt-nat-extra iptables-mod-conntrack-extra  kmod-nf-nathelper-extra
echo '
iptables -t nat -I PREROUTING -p gre -j DNAT
' >> /etc/firewall.user
## PPTP: forward initiator 1723/tcp
iptables -t nat -A prerouting_wan -p tcp --dport 1723 -j DNAT --to 192.168.4.194
iptables -A forwarding_wan -p tcp --dport 1723 -d 192.168.4.194 -j ACCEPT
## PPTP: forward tunnel GRE traffic
iptables -t nat -A prerouting_wan -p gre -j DNAT --to 192.168.4.194
iptables -A forwarding_wan -p gre -d 192.168.4.194 -j ACCEPT
```

iptables -t nat -I POSTROUTING -s 192.168.0.1/24 -o eth0 -j MASQUERADE


### debian配置ss（已测试）

<http://ntgeralt.blogspot.hk/2016/03/raspberry-pi-2-shadowsocks.html>


### dynv6更新脚本（已测试）

'''bash
crontab -e
*/1 * * * * /root/dynv6/update.sh
'''


```bash
#!/bin/sh
# send addresses to dynv6
ipv4_addr=`curl -4 -s icanhazip.com`
ipv6_addr=`curl -6 -s icanhazip.com`
echo $ipv4_addr
echo $ipv6_addr
hostname=router-kohill-001.dynv6.net
token=dThXzxHgmDYxjyaYC9KBLXuiHLjAq-
wget -6 -O- "http://dynv6.com/api/update?hostname=$hostname&ipv6=$ipv6_addr&token=$token"
wget -O- "http://ipv4.dynv6.com/api/update?hostname=$hostname&ipv4=$ipv4_addr&token=$token"

```


### Atheros网卡开启13信道（失败）
<http://luci.subsignal.org/~jow/reghack/README.txt>


### 安装带EFI支持的grub2
<https://www.douban.com/note/210077866/?type=like>
<http://bbs.wuyou.net/forum.php?mod=viewthread&tid=310626>

### 查看 UUID
sudo blkid

## xserver相关
1. Xserver https://sourceforge.net/projects/vcxsrv/
2. 在运行软件前，需要执行：
DISPLAY=192.168.1.166:0.0 startx &
export DISPLAY=:0
```bash
sudo apt-get -u install x-window-system-core
sudo apt-get -u install gdm gdm-themes
sudo apt-get -u install kde-core kde-i18n-zhcn
```
