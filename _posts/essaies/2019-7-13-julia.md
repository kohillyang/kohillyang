---
layout: post
title: Notes of julia
date: 2019-7-13 19:40
comments: true 
external-url:
categories: linux
permalink: /julia
---
<br>
### Several Tips
1. 可以在Pycharm 内安装julia 支持
<https://github.com/JuliaEditorSupport/julia-intellij>

2. Debug支持
`https://zxj5470.github.io/julia/2019/01/04/julia_en.html`
不过我没测试，不知道对julia 1.0的支持咋样

### julia 删除
需要删除： 
1. julia 的安装目录
2. %HOME%./julia
3. %HOME%./juliarc.jl
4. %HOME%./juliarc_history

### julia 安装
ubuntu 可通过ppa安装
添加下面两个ppa，
```bash
ppa:staticfloat/julianightlies
ppa:staticfloat/julia-deps
```
然后`apt install julia `


### 内置函数
`1`. randn(type, shape)
```julia
julia> rand(Float64, 1000)
1000-element Array{Float64,1}:
 0.05279877524398646
 0.8696276579595923 
 0.3090790680735598 
 ?                  
 0.8925361065681472 
 0.4795494497319175 
 0.02309618727092455

julia> rand(Float64, (1, 2))
1×2 Array{Float64,2}:
 0.0433407  0.00790523
```

`2`. broadcast(func, *args)
```julia
julia> f(x) = x + 1
f (generic function with 1 method)

julia> a = randn(Float32, 2)
2-element Array{Float32,1}:
 -0.5131272
  0.7574591

julia> broadcast(f, a)
2-element Array{Float32,1}:
 0.4868728
 1.7574592

julia> a
2-element Array{Float32,1}:
 -0.5131272
  0.7574591
```
julia 似乎对broadcast情有独钟，例如，下面的操作也是可以的：
```julia
julia> f.(a)
2-element Array{Float32,1}:
 0.4868728
 1.7574592
```
这样在一些场合可以省去大量循环。<br>
`3`. count(func, *args)

### 类型
`1`. 使用mutable struct 定义复合类型， 例如：
```julia
julia> mutable struct Person
       height
       weight
       end
```
可以使用类似构造函数的方式创建一个Person对象：
```julia
julia> mutable struct Person
       height
       weight
       end

julia> Person(0, 0)
Person(0, 0)

julia> person0 = Person(0, 1)
Person(0, 1)

julia> person0.height
0

julia> person0.weight
1

julia> person0.weight=2
2
```
julia提供了常见的数据结构，例如，可以使用Set来容纳Person对象：
```julia
julia> people = Set{Person}()
Set(Person[])

julia> push!(people, Person(0, 1))
Set(Person[Person(0, 1)])
```
可以使用循环迭代：

```julia
julia> for p $\in$ people
       print(p.weight)
       end
1
```

julia 也提供给了Dict：
```
julia> a = Dict()
Dict{Any,Any} with 0 entries

julia> a[0] = 1
1

julia> get(a, 1, 2)
2
```
`2`. Julia 提供了常用的数值类型，最低为`Int8, Uint8`， 最高为`UInt128, Int128`， 对于字面值常量，十进制默认与操作系统位数相同，且默认为有符号整型，对于八进制和十六进制，则自动地选择合适的位数：

```julia
julia> typeof(a)
Int64

julia> a = 1
1

julia> typeof(a)
Int64

julia> a = 0x12
0x12

julia> typeof(a)
UInt8

julia> a = 0x1223
0x1223

julia> typeof(a)
UInt16

julia> 
```
可以使用`bitstring`查看二进制值：
```
julia> bitstring(a)
"0001001000100011"
```
`3`. julia 提供了Bool类型，但是有一定的限制，比如将非0，1型的转成Bool会出错。

```julia
julia> Bool(1)
true

julia> Bool(1)==1
true

julia> Bool(1)==20
false

julia> Bool(1)==1
true

julia> Bool(1)==0
false

julia> Bool(20)
ERROR: InexactError: Bool(20)
Stacktrace:
 [1] Bool(::Int64) at ./float.jl:73
 [2] top-level scope at none:0
```
`4`. julia 提供了epsilon操作，对应的函数为`eps`， 可以取出某个浮点数附近的最小精度，相应的nextfloat和prevfloat可以给出某个指附近的两个最近的浮点数。
```
julia> eps(1)
ERROR: MethodError: no method matching eps(::Int64)
Closest candidates are:
  eps(::Dates.Time) at /buildworker/worker/package_linux64/build/usr/share/julia/stdlib/v1.1/Dates/src/types.jl:362
  eps(::Dates.Date) at /buildworker/worker/package_linux64/build/usr/share/julia/stdlib/v1.1/Dates/src/types.jl:361
  eps(::Dates.DateTime) at /buildworker/worker/package_linux64/build/usr/share/julia/stdlib/v1.1/Dates/src/types.jl:360
  ...
Stacktrace:
 [1] top-level scope at none:0

julia> eps(1.1)
2.220446049250313e-16

julia> eps(2.1)
4.440892098500626e-16

julia> nextfloat(2.1)
2.1000000000000005

julia> prevfloat(2.1)
2.0999999999999996

```
`5`. julia 提供了Inf和-Inf，Inf16, Inf32, Inf64来表示无穷大和无穷小，相应的，可以用isfinite(x)和isinf来判断是否为无穷。
```julia
julia> Inf()
ERROR: MethodError: objects of type Float64 are not callable
Stacktrace:
 [1] top-level scope at none:0

julia> typeof(Inf)
Float64

julia> typeof(-Inf)
Float64

julia> typeof(-Inf16)
Float16

julia> isinf(Inf)
true
```
`6`. julia 提供了Rational 来表示有理数，有理数在创建时，会自动地约分为标准形式，可以使用numerator和denominator获取其分母和分子。
```julia
julia> Rational(4, 6)
2//3

julia> Rational(4, 0)
1//0

julia> numerator(Rational(3, 6))
1

julia> denominator(Rational(3, 6))
2
```
`7`. julia 内置了对大数的支持，可以使用parse将字符串字面值转为大数，julia 不支持类型(字符串)这样的转换方式，这一点跟Python有些不同。
```julia
julia> Int32("12")
ERROR: MethodError: no method matching Int32(::String)
Closest candidates are:
  Int32(::Union{Bool, Int32, Int64, UInt32, UInt64, UInt8, Int128, Int16, Int8, UInt128, UInt16}) at boot.jl:732
  Int32(::Float32) at float.jl:700
  Int32(::Float64) at float.jl:679
  ...
Stacktrace:
 [1] top-level scope at none:0

julia> parse(BigFloat, "111")
111.0

julia> parse(BigInt, "111")
111

julia> ones(Float32, 2)
2-element Array{Float32,1}:
 1.0
 1.0

julia> ones(BigFloat, 2)
2-element Array{BigFloat,1}:
 1.0
 1.0

julia> eps(BigFloat)
1.727233711018888925077270372560079914223200072887256277004740694033718360632485e-77


```
### 运算符
1. julia 提供了 += , -=，但是注意它们都不是inplace的，调用它们会默认创建一个新的类型