---
layout: post
title: Notes of mysql
date: '2017-3-2 19:40'
comments: true
external-url: null
categories: 杂文
---
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
