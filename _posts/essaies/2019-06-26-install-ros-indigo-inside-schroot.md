---
layout: post
title: 在Ubuntu16.04中安装ubuntu14.04
date: 2019-06-25 19:40
comments: true
external-url:
categories: linux
permalink: /install-ros-indigo-inside-schroot
---
Install ros-indigo inside schroot is very useful as ubuntu 14.04 currently is unsupported, and sometimes we want to try other version of ros. Follow following steps to install it.<br>
	1. Follow http://wiki.ros.org/ROS/Tutorials/InstallingIndigoInChroot<br>
	2. Step will fail because of a bug in dpkg 1.17.5, see https://bugs.launchpad.net/snapcraft/+bug/1784558<br>
	<br>
	Something is needed to solved this issue.<br>
	Follow:
<pre>
	sudo echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates main" > /etc/apt/sources.list
	sudo apt update
	sudo apt install dpkg
</pre>This will update dpkg from 1.17.5ubuntu5 to 1.17.5ubuntu5.8<br>
    3. It's better to upgrade all existing packages using command `sudo apt upgrade`<br>
	
Some tips: <br>
	1. schoot will execute all commands exit in /etc/schroot/setup.d/ on host. <br>
	2. Dependece problem may be hard to solve in ubuntu-14.04, so it is better to use aptitude instead of apt or apt-get.<br>
	3. sudo debootstrap --variant=buildd --arch=amd64 trusty /srv/chroot/indigo_trusty https://mirrors.tuna.tsinghua.edu.cn/ubuntu/<br>
	4. Use following commands with 'if' to setup ros environment values instead:<br>
```bash
	if [ "$SCHROOT_UID" != "1000" ]; then
	  schroot -c indigo_trusty
	else
	  export ROS_MASTER_URI="http://localhost:11311"
	  source /opt/ros/indigo/setup.sh
	  export DISPLAY=:0
	  echo "hello world"
	  export | grep ROS
```
Some errors may occur:<br>
`1`. `start: Unable to connect to Upstart: Failed to connect to socket /com/ubuntu/upstart: Connection refused`
<pre>
	sudo dpkg-divert --local --rename --add /sbin/initctl
	 ln -s /bin/true /sbin/initctl
</pre>
`2`. `Missing headers`:
	I solved it by:

```bash
	sudo apt-get install linux-headers-4.4.0-38-generic

	sudo apt-get -f install
```

Other tips:<br>
 Setup Gazebo Models URI of gazebo has changed from http://gazebosim.org/models/ to http://models.gazebosim.org, we have to download the models manually. Follow: <https://blog.csdn.net/qq_16397695/article/details/52767184>





