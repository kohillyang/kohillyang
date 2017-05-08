---
layout: post
title: Mysql
date: '2017-3-2 19:40'
comments: true
external-url: null
categories: python mysql
---
<br>

### 尽量使用参数化查询插入
比如`cursor2.execute(sqlI,tuple(value))`实际上等效于：

```python
sqlI = sql % tuple(map(db.escape_string,value))
cursor2.execute(sqlI)
```
因此参数化查询更不容易出错
<div class="alert alert-warning">
！注意表名，列名带有desc等关键字时，要用``围起来。
</div>

### 表的新建&删除
新建表：`CREATE TABLE profile_expand (id int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id));`

```python
sql = 'CREATE TABLE %s (id int(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)) CHARSET=utf8 ;'%(tableName,)
cursor.execute(sql)
```
删除表：`DROP TABLE profile_expand`

### 列的新建

新建列：$\text{alter table profile_expand add 'key' text }$
<div class="alert alert-warning">
！注意表名，列名带有desc等关键字时，要用``围起来。
</div>

### 查询函数

```python
cursor.execute('SELECT COUNT(id) FROM profile;')
print('Total Available Rows:' + str(cursor.fetchone()[0]))
```

### 表查询

```python
cursor.execute('SELECT id,type,profile,query_time,level FROM profile LIMIT 1000')
for line in cursor.fetchall():
    js = json.loads(line[2])
    pprint(js)
```

### 行数查询
<code>SELECT COUNT(`id`) FROM probability_nickname;<code>


### debian 安装mysql并允许远程登录

```bash
apt-get install mysql-server
```
2.登录数据库
mysql -u root -p

输入密码
mysql> use mysql;


3.查询host
mysql> select user,host from user;


4.创建host
如果没有"%"这个host值,就执行下面这两句:
mysql> update user set host='%' where user='root';
mysql> flush privileges;


5.授权用户
任意主机以用户root和密码mypwd连接到mysql服务器
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'mypwd' WITH GRANT OPTION;
mysql> flush privileges;

IP为192.168.1.102的主机以用户myuser和密码mypwd连接到mysql服务器
mysql> GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'192.168.1.102' IDENTIFIED BY 'mypwd' WITH GRANT OPTION; 
mysql> flush privileges;

#### mysql 重置密码

1.停止MySQLd；
    sudo /etc/init.d/MySQL stop
(您可能有其它的方法,总之停止MySQLd的运行就可以了)
2.用以下命令启动MySQL，以不检查权限的方式启动；
    MySQLd --skip-grant-tables &
3.然后用空密码方式使用root用户登录 MySQL；
    MySQL -u root
4.修改root用户的密码；
    MySQL> update MySQL.user set password=PASSWORD('newpassword') where User='root';  
    MySQL> flush privileges;  
    MySQL> quit 
重新启动MySQL
    /etc/init.d/MySQL restart
就可以使用新密码 newpassword 登录了。



### Lost connection to MySQL server during query

<http://stackoverflow.com/questions/1884859/lost-connection-to-mysql-server-during-query>