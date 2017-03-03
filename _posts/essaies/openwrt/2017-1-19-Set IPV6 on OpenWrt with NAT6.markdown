---
layout: post
title: Set IPV6 on OpenWrt with NAT6
date: 2017-01-09 15:46
comments: true
external-url:
categories: OpenWrt
---
<br>
## Set IPv6
　　把下面的代码放入任意目录，比如存入`/tmp/nat_set.sh`，并执行`chmod +x /tmp/nat_set.sh`以给文件加上可执行权限，最后`./tmp/nat_set.sh`以执行该脚本。<br><br>

```bash
#!/bin/sh /etc/rc.common
# NAT6 init script for OpenWrt // Depends on package: kmod-ipt-nat6
wget -P /etc/init.d/ http://cdn.rawgit.com/kohillyang/personal-blog/master/assets/openwrt/nat6
opkg update
opkg install kmod-ipt-nat6
uci set network.globals.ula_prefix="$(uci get network.globals.ula_prefix | sed 's/^./d/')"
uci commit network
uci set dhcp.lan.ra_default='1'
uci commit dhcp
chmod +x /etc/init.d/nat6
/etc/init.d/nat6 enable
uci set firewall.@rule["$(uci show firewall | grep 'Allow-ICMPv6-Forward' | cut -d'[' -f2 | cut -d']' -f1)"].enabled='0'
uci commit firewall
reboot
```
<br>
　　稍后路由器会自动重启，重启之后等待半分钟左右，在shell中执行`logread | grep NAT6`查看结果：<br>
  <img src="http://ok0rtur47.bkt.clouddn.com/2017-1-17-image003.png"  class="img-responsive center-block" style="width:100%"><br>
　　一切正常的话，这时候电脑应该能正常访问ipv6站点了。
<br>

<strong> References</strong>

　　本文中的方法参考[2]， 如果本文有叙述不清楚的地方，可以进入原文查看，但注意原文中的脚本需要修改。如果希望纯手动设置，可参考[1]，[3]中是关于openwrt连上v6的办法，如果您的路由器无法连上v6，可以按此文中的办法设置。<br>
[1]. [OpenWRT 路由器作为 IPv6 网关的配置](https://github.com/tuna/ipv6.tsinghua.edu.cn/blob/master/openwrt.md).<br>
[2]. [ NAT6: IPv6 Masquerading Router](https://wiki.openwrt.org/doc/howto/ipv6.nat6).<br>
[3]. [OpenWrt native IPv6-stack](https://wiki.openwrt.org/doc/uci/network6).
<br>


## Install Transmission
　　电脑能正常访问IPv6之后，可以在电脑上访问北邮之类的Bt站点了，也可以利用路由器来做种，由于Transmission体积较大，大部分路由器是没办法直接安装的，这时候需要利用linux的overlay技术把系统镜像到外部磁盘，可以参见[Rootfs on External Storage (extroot)](https://wiki.openwrt.org/doc/howto/extroot)，安装transmission的方法参见
<a href="https://wiki.openwrt.org/doc/uci/transmission">Transmission configuration</a>，配置samba的方法参见[OpenWrt Samba 共享配置](http://www.jebbs.co/2015/06/09/openwrt-samba/)。<br>
　　以上链接本人在14.07的openwrt上都测试没有任何问题。路由器是Dir825,8MByte Flash+61348kB RAM，CPU是AR7161，个人感觉CPU比较弱，导致我跑Samba只有11MB/s左右。<br>
　　可以看到cpu全被Samba占了，所以在此提醒各位，路由器配置太重要了。
<img src="{{ site.cdn_prefix }}/screenshots/2017-2-9-0002.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%">

　　用vsftpd的话cpu占用率会低一些，大概60%左右，但是速度还是11MB/s，原因就不太清楚了，同款路由器网上ftp是可以跑到25MB/s 以上的。
<img src="{{ site.cdn_prefix }}/screenshots/2017-2-9-0004.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%">

<strong>关于transmission的一些注意事项</strong>
<br>
<br>
1. 由于内存分配的原因（小内存机器可能还需要配置交换分区），transmission启动时可能会发生内存申请不成功的情况，请尝试在<code>/etc/sysctl.conf</code>中加入如下代码：

```bash
# handle rtorrent related low memory issues
vm.swappiness=95
vm.vfs_cache_pressure=200
vm.min_free_kbytes=4096
vm.overcommit_memory=2
vm.overcommit_ratio=60

net.core.wmem_max = 1048576
net.core.rmem_max = 4194304
```
　　注意改了之后重启路由器才会生效。
<br>
2. transmission可以在luci中加入图形化配置菜单，命令为：`opkg install luci-app-transmission`，客户端从[transmission Remote GUI](https://sourceforge.net/projects/transgui/postdownload?source=dlp)下载。<br>
3. 测试成功的transmission配置文件[点我下载]({{ site.github_cdn_prefix }}/openwrt/conf_file/transmission.conf)。<br>
<br>
4. 如果需要封锁IPv4访问，可在防火墙中将访问51413端口的包拒绝掉即可。
<br>
5. 关于交换分区的设置，需要先在硬盘上分一个跟内存差不多大小的交换分区，确认路由器可以正常挂载硬盘之后：
`block detect > /etc/config/fstab`<br>
使用命令`cat /etc/config/fstab`查看自动识别的分区是否正确（保留Swap项即可）：
<img src="{{ site.cdn_prefix }}/screenshots/2017-2-10-0001.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%">
<br>
　　让它开机自动挂载：`/etc/init.d/fstab enable`<br>
　　执行`reboot`使路由器重启，随后执行`free`可以看到交换分区大小：
<img src="{{ site.cdn_prefix }}/screenshots/2017-2-10-0002.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%"><br>
　　具体参考[Fstab Configuration](https://wiki.openwrt.org/doc/uci/fstab#addingswappartitions)。<br>
　　配置完overlay以及swap后，效果图是这样的：
<img src="{{ site.cdn_prefix }}/screenshots/2017-2-10-0004.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%"><br>
　　如果不希望在硬盘上分交换分区，可以用文件作交换分区：

```
dd if=/dev/zero of=/mnt/sda1/swapfile bs=1024 count=62142
mkswap /mnt/sda1/swapfile
swapon /mnt/sda1/swapfile
```
　　效果图：
<img src="{{ site.cdn_prefix }}/screenshots/2017-2-10-0008.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%">
<br>

　　还是挺费CPU资源的：

<img src="{{ site.cdn_prefix }}/screenshots/2017-2-10 0000.jpg" class="img-ressponssive" style="width: 90%;margin-left: 3%">
<br>　　

## Install Aria2 .
　　因为CPU性能原因，相比之下，Aria2要轻巧很多，官方的Aria2取消了Bt的支持，因此需要自行编译，编译方法参考[编译openwrt平台aria2的最新版](http://www.jianshu.com/p/1042483f90fe);
　　我自用的Aria2版本是1.31.0，SSH登录Openwrt以后，用以下脚本安装，DOWNLOAD_SITE对于AR71xx的CPU不需要更改，CONF_PATH根据自己配置文件路径更改，非AR71xx的机型到[Packages](https://github.com/kohillyang/personal-blog/tree/master/assets/openwrt/packages/have_not_been_tested/aria2-1.18.3)手动下载安装。

```bash
#!/bin/sh /etc/rc.common
DOWNLOAD_SITE="{{ site.github_cdn_prefix }}/openwrt/packages/have_tested/aria2_1.31.0-1_ar71xx.ipk"
CONF_PATH=/mnt/aria2/aria2.conf
cd /tmp
opkg update
wget -O aria2.ipk $DOWNLOAD_SITE
wget -O $CONF_PATH {{ site.github_cdn_prefix }}/openwrt/conf_file/aria2.conf
opkg install aria2.ipk
echo '#!/bin/sh /etc/rc.common
START=60
CONF_PATH=$CONF_PATH
boot() {
    aria2c --conf-path=$CONF_PATH -D
}

start(){
    aria2c --conf-path=$CONF_PATH -D
}

stop(){
    killall aria2c
}' > /etc/init.d/aria2
chmod +x /etc/init.d/aria2
/etc/init.d/aria2 enable
/etc/init.d/aria2 start
```

适用于小米路由器的脚本

```bash
#!/bin/sh /etc/rc.common
DOWNLOAD_SITE="https://github.com/kohillyang/personal-blog/blob/master/assets/openwrt/packages/have_not_been_tested/aria2_1.31.0-1_ramips_24kec.ipk"
opkg update
wget -O aria2.ipk $DOWNLOAD_SITE
opkg install aria2.ipk
cd /root
mkdir aria2
CONF_PATH=/root/aria2/aria2.conf
wget -O $CONF_PATH {{ site.github_cdn_prefix }}/openwrt/conf_file/aria2.conf
echo '#!/bin/sh /etc/rc.common
CONF_PATH=/root/aria2/aria2.conf
START=60
boot() {
    aria2c --conf-path=$CONF_PATH -D
}

start(){
    aria2c --conf-path=$CONF_PATH -D
}

stop(){
    killall aria2c
}' > /etc/init.d/aria2
chmod +x /etc/init.d/aria2
/etc/init.d/aria2 enable
/etc/init.d/aria2 start
```

访问[WebUI](http://dy.ghostry.cn/)或者[Aria2 Web Interface](https://qcloud.kohill.cn/aria2/)即可看到控制台，注意https下Chrome可能会拦截与路由器（http://192.168.1.1:6800） 之间的非安全连接，请手动允许。<br>
　　配置文件解释:[aria2 Documation](https://aria2.github.io/manual/en/html/aria2c.html#cmdoption-V)。<br>
<img src="{{ site.github_cdn_prefix }}/screenshots/2017-2-15 0000.jpg" class="img-responssive"><br>

## Some IPv6 sites

1. [清华大学镜像站](https://mirrors.tuna.tsinghua.edu.cn/).
2. [谷歌ipv6站](https://ipv6.google.com).
3. [facebook ipv6站](https://www.v6.facebook.com/).

## Something about Xioami Router

Please see [小米路由器mini折腾之配置opkg篇](https://blog.phpgao.com/xiaomi_router_opkg.html)

关键是更改/etc/opkg.conf

```bash
dest root /
dest ram /tmp
lists_dir ext /etc/opkg-lists
option overlay_root /overlay

arch all 100
arch ramips_24kec 200
arch ramips 300
arch mips 400
arch unkown 500


src/gz barrier_breaker_base http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/base
src/gz barrier_breaker_luci http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/luci
src/gz barrier_breaker_management http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/management
src/gz barrier_breaker_oldpackages http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/oldpackages
src/gz barrier_breaker_packages http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/packages
src/gz barrier_breaker_routing http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/routing
src/gz barrier_breaker_telephony http://downloads.openwrt.org/barrier_breaker/14.07/ramips/mt7620a/packages/telephony
```

## 其他IPV6设置方法
使用ndp代理
<http://www.openwrt.org.cn/bbs/forum.php?mod=viewthread&tid=7116><br>

<http://www.right.com.cn/forum/thread-100010-1-1.html><br>

ndppd<http://bbs.swdyz.com/thread270sw1dyz1.shtml>

ip6nat<https://sourceforge.net/projects/ipv6nat/?source=typ_redirect>

Native Stack

<https://wiki.openwrt.org/doc/uci/network6>

[WAN口获取单一IPv6地址时，内网使用IPv6的方法（教育网可用）](http://koolshare.cn/thread-24920-1-1.html)

> 整理

```bash
/ect/config/network:
config interface 'loopback'
        option ifname 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
        option ula_prefix 'fd3c:2dd9:5114::/48'

config interface 'lan'
        option ifname 'eth0'
        option force_link '1'
        option type 'bridge'
        option proto 'static'
        option ipaddr '192.168.1.1'
        option netmask '255.255.255.0'
        option ip6assign '60'

config interface 'wan'
        option ifname 'eth1'
        option proto 'dhcp'

config interface 'wan6'
        option ifname 'eth1'
        option proto 'dhcpv6'

config switch
        option name 'switch0'
        option reset '1'
        option enable_vlan '1'

config switch_vlan
        option device 'switch0'
        option vlan '1'
        option ports '0 1 2 3 4'

/etc/config/dhcp:


config dnsmasq
        option domainneeded '1'
        option boguspriv '1'
        option filterwin2k '0'
        option localise_queries '1'
        option rebind_protection '1'
        option rebind_localhost '1'
        option local '/lan/'
        option domain 'lan'
        option expandhosts '1'
        option nonegcache '0'
        option authoritative '1'
        option readethers '1'
        option leasefile '/tmp/dhcp.leases'
        option resolvfile '/tmp/resolv.conf.auto'
        option localservice '1'

config dhcp 'lan'
        option interface 'lan'
        option start '100'
        option limit '150'
        option leasetime '12h'
        option dhcpv6 'hybrid'
        option ra 'hybrid'
        option ndp 'hybrid'

config dhcp 'wan'
        option interface 'wan'
        option ignore '1'

config odhcpd 'odhcpd'
        option maindhcp '0'
        option leasefile '/tmp/hosts/odhcpd'
        option leasetrigger '/usr/sbin/odhcpd-update'

config dhcp 'wan6'
        option interface 'wan'
        option dhcpv6 'hybrid'
        option ra 'hybrid'
        option ndp 'hybrid'
        option master '1'
```

relay

```bash
作者：钟子乎
链接：https://www.zhihu.com/question/29667477/answer/93634257
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

config dhcp 'lan'
	option interface 'lan'                   
	option start '100'                       
	option limit '150'                       
	option leasetime '12h' 
	option ra 'relay'                                            
	option ndp 'relay'
	option dhcpv6 'relay'
	
config dhcp 'wan'                                
	option interface 'wan'                   
	# default value is '0', uncomment it if you want to ignore this interface
	# option ignore '1'

config dhcp 'wan6'
	option interface 'wan'
	option ra 'relay'                        
	option ndp 'relay'  
	option dhcpv6 'relay'  
	option master '1'
```

```bash
config dhcp 'lan' 
	option interface 'lan' 
	option start '100' 
	option limit '150' 
	option leasetime '12h' 
	option ra 'hybrid' 
	option dhcpv6 'hybrid' 
	option ndp 'hybrid' 
	option ra_management '1' 

config dhcp 'wan6' 
	option interface 'wan' 
	option dhcpv6 'hybrid' 
	option ra 'hybrid' 
	option ndp 'hybrid' 
	option master '1'

作者：Zhangjun Liu
链接：https://www.zhihu.com/question/29667477/answer/47149165
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

```bash
环境：
wan口 eth1
lan口 br-lan
wan对外网关：2001:250:1006:3006::1/64
lan内客户端1：2001:250:1006:3006:2::20/80
lan内客户端2：2001:250:1006:3006::2::21/80
客户端网关：路由器lan口v6地址（没有手动设置一个）。
 
#设置系统支持：
sysctl -w net.ipv6.conf.all.forwarding=1  #其他发行版需要开启ipv6包转发；openwrt默认就是会转发的，这句可忽略。
sysctl -w net.ipv6.conf.all.proxy_ndp=1   #开启邻居代理功能，如果使用npd6的话，这句可忽略。
#设置路由支持：

ip -6 route add 2404:6800:4008:800::200e/128 via fe80::cecc:81ff:fec0:d75d dev pppoe-wan metric 0 
ip -6 route add 2000::/3 via fe80::cecc:81ff:fec0:d75d dev pppoe-wan metric 1  #wan口默认路由

ip -6 route add 2001:250:1001:2500:2037::/80 dev br-lan metric 0  #将发往lan内客户端的数据交给lan口
ip -6 route add 2001:250:1001:2500:a888::/80 dev br-lan metric 0  #将发往lan内客户端的数据交给lan口
#ndp设置：
ip -6 neigh add proxy 2001:250:1001:2500:2037:f4d:1dc8:e7c8 dev pppoe-wan    #在wan口开启对PC1的邻居代理
ip -6 neigh add proxy 2001:250:1001:2500:a888:af6:36c5:a8cf dev pppoe-wan    #在wan口开启对PC2的邻居代理

。。。。。。有多少设备上ipv6就需要设置几条ndp规则
 
然后，你要上网的电脑，配置ipv6的ip、网关：填写路由lan口ipv6地址、dns （如he的dns：2001:470:20::2）
```

## FeedBack

　　本文不开放评论，如果对本文有任何疑问，可以到[这儿](https://github.com/kohillyang/personal-blog/issues)提交issue或者给本人发送邮件，邮件地址在网页最下方。
