---
layout: post
title: Add https support for web server
date: 2017-02-14 19:40
comments: true
external-url:
categories:  linux
permalink: /add_https_for_web_server
---
<br>

[参考链接](https://jayshao.com/lets-encrypt-mian-fei-https-zheng-shu-shi-yong-zhi-nan/)

### 执行以下命令
路由器需要添加tls支持

```bash
opkg update && opkg install uhttpd-mod-tls
```

```bash
git clone https://github.com/letsencrypt/letsencrypt
cd letsencrypt
./certbot-auto certonly

```
根据提示操作即可，需要一个debian或者ubuntu等支持apt-get的系统

根据你的选择会在/etc/letsencrypt下产生证书，私钥等

根据web服务器配置即可

`/etc/config/uhttpd`

```bash
# Server configuration
config uhttpd main
	# HTTP listen addresses, multiple allowed
	list listen_http 0.0.0.0:80
	# list listen_http [::]:80
	# HTTPS listen addresses, multiple allowed
	list listen_https 0.0.0.0:443
	# list listen_https [::]:443
	# Server document root
	option home  /www
	# Reject requests from RFC1918 IP addresses
	# directed to the servers public IP(s).
	# This is a DNS rebinding countermeasure.
	option rfc1918_filter 0
	# Certificate and private key for HTTPS.
	# If no listen_https addresses are given,
	# the key options are ignored.
	option redirect_https	1
	option cert  /root/utttp/fullchain.pem
	option key  /root/utttp/privkey.pem
	# CGI url prefix, will be searched in docroot.
	# Default is /cgi-bin
	option cgi_prefix /cgi-bin
```

### 之前的办法

本文在Nginx上测试成功

```bash
openssl genrsa 4096 > account.key
openssl genrsa 4096 > domain.key
#openssl ecparam -genkey -name secp256r1 | openssl ec -out domain.key
openssl req -new -sha256 -key domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:yoursite.com,DNS:www.yoursite.com")) > domain.csr
```
假设www是你的网站目录

```bash
mkdir www/challenges/
```
在Nginx上创建一个Server，配置文件：

```bash
server {
    server_name www.yoursite.com yoursite.com;

    location ^~ /.well-known/acme-challenge/ {
        alias /home/xxx/www/challenges/;
        try_files $uri =404;
    }

    location / {
        rewrite ^/(.*)$ https://yoursite.com/$1 permanent;
    }
}
```

继续执行下面的命令：

```bash
wget https://raw.githubusercontent.com/diafygi/acme-tiny/master/acme_tiny.py
python acme_tiny.py --account-key ./account.key --csr ./domain.csr --acme-dir ~/www/challenges/ > ./signed.crt
wget -O - https://letsencrypt.org/certs/lets-encrypt-x1-cross-signed.pem > intermediate.pem
cat signed.crt intermediate.pem > chained.pem
```

在nginx下配置证书，示例如下：

```bash
# You may add here your
# server {
#   ...
# }
# statements for each of your virtual hosts to this file

##
# You should look at the following URL's in order to grasp a solid understanding
# of Nginx configuration files in order to fully unleash the power of Nginx.
# http://wiki.nginx.org/Pitfalls
# http://wiki.nginx.org/QuickStart
# http://wiki.nginx.org/Configuration
#
# Generally, you will want to move this file somewhere, and start with a clean
# file but keep this around for reference. Or just disable in sites-enabled.
#
# Please see /usr/share/doc/nginx-doc/examples/ for more detailed examples.
##

server {
        listen   80;
        root /home/uftp/www;
        index index.php index.html index.htm;
        server_name qcloud.kohill.cn;
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;
    ssl_certificate     /home/ubuntu/https_lets_encrypt/chained.pem;
    ssl_certificate_key /home/ubuntu/https_lets_encrypt/domain.key;
        location = /50x.html {
              root /usr/share/nginx/www;
        }
        # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
        location ~ \.php$ {
                try_files $uri =404;
                #fastcgi_pass 127.0.0.1:9000;
                # With php5-fpm:
                fastcgi_pass unix:/var/run/php5-fpm.sock;
                fastcgi_index index.php;
                include fastcgi_params;
         }
        location ^~ /.well-known/acme-challenge/ {
                alias /home/uftp/www/challenges/;
                try_files $uri =404;
        }

        location / {
                rewrite ^/(.*)$ https://qcloud.kohill.cn/$1 permanent;
        }


}

# another virtual host using mix of IP-, name-, and port-based configuration
#
#server {
#   listen 8000;
#   listen somename:8080;
#   server_name somename alias another.alias;
#   root html;
#   index index.html index.htm;
#
#   location / {
#       try_files $uri $uri/ =404;
#   }
#}


# HTTPS server

server {
    listen 443;
    server_name localhost;

#   root html;
        root /home/uftp/www;
    index index.html index.htm;

    ssl on;
#   ssl_certificate cert.pem;
#   ssl_certificate_key cert.key;
        ssl_certificate     /home/ubuntu/https_lets_encrypt/chained.pem;
        ssl_certificate_key /home/ubuntu/https_lets_encrypt/domain.key;


    ssl_session_timeout 5m;

    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers "HIGH:!aNULL:!MD5 or HIGH:!aNULL:!MD5:!3DES";
    ssl_prefer_server_ciphers on;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### nginx设置网址重定向

```json
server{
	location / {
		rewrite ^/ http://notes.kohill.cn;
	}
}
```
