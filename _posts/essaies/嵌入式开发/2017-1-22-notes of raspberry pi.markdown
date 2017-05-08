---
layout: post
title: Raspberry Pi
date: 2017-01-22 19:40
comments: true
external-url:
categories: linux
---
<br>

1. 树莓派在默认情况下不开ssh，需要在boot分区下新建一个文件名为ssh的文件。<br>
2. 使用windows远程桌面连接：`sudo apt-get install xrdp`，之后直接输入ip即可(可能需要重启)。<br>
3. 安装vnc server:`sudo apt-get install tightvncserver`,用`vncserver -geometry 1024x768`连接。<br>
4. 打开spi使用`sudo raspi-config`，选择打开spi即可<br>
5. 在`https://pypi.python.org/pypi/spidev/3.1`上下载python库，使用`sudo python3 setup.py install`安装
6. 树莓派有为树莓派封装的gpio库`https://pypi.python.org/pypi/RPi.GPIO`<br>编译的时候如果没有找到python.h，则需要安装`sudo apt-get install python-dev`<br>
7. python下树莓派提供的nrf24l01的库`git clone https://github.com/riyas-org/nrf24pihub`<br>
8. 安装vsftpd，直接`sudo apt-get install vsftpd`，在`/etc/vsftpf.conf`中打开写权限，随后`sudo service vsftpd start`。
<br>

```python
#!/usr/bin/env python
 
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
while True:
 
     GPIO.output(11,True)
 
     time.sleep(1)
     GPIO.output(11,False)
     time.sleep(1)
```
<br>
主机发送:<br>

```python
from nrf24 import NRF24
import time
from time import gmtime, strftime
 
#设定从机的发送地址pipes[0],pipes[1],本机的发送pipes[0]
pipes = [[0x10, 0x10, 0x10, 0x10, 0x20], [0x10, 0x10, 0x10, 0x10, 0x22]]
radio = NRF24()
radio.begin(0, 0,25,18) #set gpio 25 as CE pin,gpio 18 as IRQ pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
 
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
 
radio.startListening()
radio.stopListening()
 
radio.printDetails()
radio.startListening()
 
while True:
 
    pipe = [0] #pipe为接收到的信息的从机从机身份标识
    while not radio.available(pipe, True):
        time.sleep(100/1000000.0)
    recv_buffer = []
    radio.read(recv_buffer)
    out = ''.join(chr(i) for i in recv_buffer)
    print "Message from "+str(pipe[0])+":"+out

```
<br>

从机接收:<br>

```python
from nrf24 import NRF24
import time
from time import gmtime, strftime
pipes = [[0x10, 0x10, 0x10, 0x10, 0x20], [0x10, 0x10, 0x10, 0x10, 0x12]]
radio = NRF24()
radio.begin(0, 0,25,18) #set gpio 25 as CE pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
 
radio.startListening()
radio.stopListening()
 
radio.printDetails()
radio.startListening()
count = 1
while True:
    pipe = [0]
    send_data = "send count: "+str(count)
    print "start send data..."
    print "send data:"+str(count)
    radio.stopListening()
    ok = 0
    ok_true = 32
    while ok!=ok_true:
        ok = radio.write(send_data)
    time.sleep(2)
    count = count + 1
```
<br>
nrf24提供的示意代码：
<br>

```python
#!/usr/bin/python
# raspberry pi nrf24l01 hub
# more details at http://blog.riyas.org
# Credits to python port of nrf24l01, Joao Paulo Barrac & maniacbugs original c library

from nrf24 import NRF24
import time
from time import gmtime, strftime

pipes = [[0xf0, 0xf0, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xd2]]

radio = NRF24()
radio.begin(0, 0,25,18) #set gpio 25 as CE pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

radio.startListening()
radio.stopListening()

radio.printDetails()
radio.startListening()

while True:
    pipe = [0]
    while not radio.available(pipe, True):
        time.sleep(1000/1000000.0)
    recv_buffer = []
    radio.read(recv_buffer)
    out = ''.join(chr(i) for i in recv_buffer)
    print out
    

```
<br>


所使用的连接：<br>

| 树莓派 	    | nrf24l01   |
|-------------|------------|
|   CE        |   GPIO.0   |
|   IRQ       |   GPIO.1   |

运行示例程序，打印出以下信息：<br>
<img src="http://ok0rtur47.bkt.clouddn.com/2017-1-22-image001.png" class="img-responsive center-block" style="width:100%">

关闭应答下的单片机端初始化程序：
<br>

```cpp
	SPI_CE_L();
	unsigned char rtaddr[]={0x01,0x02,0x03,0x02,0x01};
//	NRF_Write_Buf(NRF_WRITE_REG+RX_ADDR_P0,rtaddr,sizeof(rtaddr));//写RX节点地址
	NRF_Write_Buf(NRF_WRITE_REG+TX_ADDR,rtaddr,sizeof(rtaddr)); //写TX节点地址
	NRF_Write_Reg(NRF_WRITE_REG+EN_AA,0x00); //关闭通道0的自动应答
	NRF_Write_Reg(NRF_WRITE_REG+EN_RXADDR,0x00);//使能通道0
	NRF_Write_Reg(NRF_WRITE_REG+SETUP_RETR,0x00);//关闭自动重发
	NRF_Write_Reg(NRF_WRITE_REG+RF_CH,40); //设置RF通道为CHANAL
	NRF_Write_Reg(NRF_WRITE_REG+RX_PW_P0,RX_PLOAD_WIDTH);//选择通道0的有效数据宽度 
	NRF_Write_Reg(NRF_WRITE_REG+RF_SETUP,0x0f);
	NRF_Write_Reg(NRF_WRITE_REG+SETUP_AW,0x03);  //总共5byes地址
	NRF_Write_Reg(NRF_WRITE_REG + CONFIG, 0x0e);   		 // IRQ收发完成中断响应，16位CRC，主发送
	
	SPI_CE_H();
```

<br>
树莓派端接收程序：
<br>

```python
#coding=utf-8
'''
@author: kohill
'''
from nrf24 import NRF24
import time
from time import gmtime, strftime
 
#设定从机的发送地址pipes[0],pipes[1],本机的发送pipes[0]
pipes = [[0x01,0x02,0x03,0x02,0x01], [0x01,0x02,0x03,0x02,0x01]]
radio = NRF24()
radio.begin(0, 0,22,23) #set gpio 25 as CE pin,gpio 18 as IRQ pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(40)
radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(0)

radio.openReadingPipe(0, pipes[0])
radio.startListening()
radio.stopListening()
 
radio.printDetails()
radio.startListening()
 
while True:
 
    pipe = [0] #pipe为接收到的信息的从机从机身份标识
    while not radio.available(pipe, True):
        time.sleep(100/1000000.0)
    recv_buffer = []
    radio.read(recv_buffer)
    out = ''.join(chr(i) for i in recv_buffer)
    print "Message from "+str(pipe[0])+":"+out

```

<br>



## 参考链接：

1. [基于NRF24L01实现两个树莓派和一个Beaglebone Black组网通讯](https://www.embbnux.com/2014/12/18/two_raspberry_pi_and_a_beaglebone_black_communicate_on_nrf24l01_network/)
2. [Learn from the fly](http://www.riyas.org/2014/08/raspberry-pi-as-nrf24l01-base-station-internet-connected-wireless.html)
3. [看了你就会了](http://www.51hei.com/bbs/dpj-29549-1.html)
<br><br>