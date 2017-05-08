---
layout: post
title: R Language
date: 2017-05-21 15:46
comments: true
external-url:
categories: linux
---
<br>


1. 产生服从正态分布的随机数
`vec <- rnorm(100)`
2. 从随机数中挑出大于0.5的数
`vec[vec>0.5]`



### example1，绘制一个大型网络的局部图

```R
# read.table("E://snap/examples/node2vec/graph/karate.edgelist",header= FALSE,sep = " ",colClasses =c("character","character"))->g
# g2<-na.omit(g)
library(igraph) #
# x<-par(bg="black") #
# g2 = graph.data.frame(d = g2,directed = F); 
# V(g2) #
# E(g2) #
# op <- par(mar = rep(0, 4))   
# plot.new()
# par(op)
# # E(g2)$color=V(g2)[name=ends(g2,E(g2))[,2]]$color #
# # V(g2)[grep("1",V(g2)$name)]$color=rgb(1,1,1,0.8) #
# g1 <- g2
# E(g1)$color=V(g1)[name=ends(g1,E(g1))[,1]]$color #
# V(g1)[grep("1",V(g1)$name)]$color=rgb(1,1,1,0.8) #
# plot(g1,layout=layout.fruchterman.reingold,vertex.size=V(g1)$size,edge.width=0.3,edge.color = E(g1)$color,vertex.frame.color=NA,margin= rep(0, 4),vertex.label=NA)

friends.whole <- read.table("E://snap/examples/node2vec/graph/karate.edgelist", header=FALSE, sep=" ", col.names=c("from","to"))
library(igraph)

sort(table(c(friends.whole$from, friends.whole$to)), dec=T)

uid <- 1082953
uid2 <- 199312

# friends.connected <- unique(c(
#   friends.whole$to[friends.whole$from == uid], 
#   friends.whole$from[friends.whole$to == uid2]))

friends.connected<- c(friends.whole$from[1:200],friends.whole$to[1:200])
# friends.connected <- unique(c(
#   friends.whole$to[friends.whole$from == uid], 
#   friends.whole$from[friends.whole$to == uid2]))
friends.sample <- friends.whole[
((friends.whole$from %in% friends.connected) | 
(friends.whole$to %in% friends.connected)), c(1,2)]

friends.graph <- graph.data.frame(d = friends.sample, 
directed = F, vertices = unique(c(friends.sample$from, 
                                  friends.sample$to)))

friends.graph <- simplify(friends.graph)
is.simple(friends.graph)

dg <- degree(friends.graph)
friends.graph <- induced.subgraph(friends.graph, 
                                  which(dg > 0))
# plot(friends.graph, 
#      layout = layout.fruchterman.reingold, 
#      vertex.size = 2.5, 
#      vertex.frame.color=NA,
#      vertex.label = NA, 
#      edge.color = grey(0.5), 
#      edge.arrow.mode = "-")
friends.com = walktrap.community(friends.graph, steps=10)

V(friends.graph)$sg = friends.com$membership

V(friends.graph)$color = NA
V(friends.graph)$color = rainbow(max(V(friends.graph)$sg))[V(friends.graph)$sg]

plot(friends.graph, layout = layout.fruchterman.reingold, 
     vertex.size = 5, vertex.color = V(friends.graph)$color, 
     vertex.label = NA, edge.color = grey(0.5), edge.arrow.mode = "-")
V(friends.graph)$btn = betweenness(friends.graph, directed = F)
plot(V(friends.graph)$btn, xlab="Vertex", ylab="Betweenness")
V(friends.graph)$size = 5
V(friends.graph)[btn>=500]$size = 15
V(friends.graph)$label = NA
V(friends.graph)[btn>=500]$label = V(friends.graph)[btn>=500]$name

plot(friends.graph, layout = layout.fruchterman.reingold, 
     vertex.size = V(friends.graph)$size, 
     vertex.color = V(friends.graph)$color, 
    #  vertex.label = V(friends.graph)$label, 
     vertex.label = NA,     
     edge.color = grey(0.5),
     edge.arrow.mode = "-")
```


### Example 计算ROC
<https://cran.r-project.org/web/packages/PRROC/vignettes/PRROC.pdf>

```R
## computing a simple pr curve (x-axis: fpr, y-axis: tpr)
read.table("I://node2vec/direct_auc.txt",
            header= FALSE,
            sep = " ",
            colClasses =c("numeric","integer"),
            col.names = c("predict","target"))->g
library(pROC)
plot.roc(g$target, g$predict)
plot.roc(c(1,1,0,0),c(0.5,0.6,0,0))
auc(g$target, g$predict)
```

绘制pr曲线
<https://cran.r-project.org/web/packages/ROCR/ROCR.pdf>

```
## computing a simple pr curve 
read.table("direct_auc_intersect.txt",
            header= FALSE,
            sep = " ",
            colClasses =c("numeric","integer"),
            col.names = c("predict","target"))->g
library(ROCR)
pred <- prediction( g$predict, g$target)
perf <- performance(pred,"tpr","fpr")
plot(perf)
## precision/recall curve (x-axis: recall, y-axis: precision)
perf1 <- performance(pred, "prec", "rec")
plot(perf1)
## sensitivity/specificity curve (x-axis: specificity,
## y-axis: sensitivity)
#perf1 <- performance(pred, "sens", "spec")
#plot(perf1)
```

AUPRC is a function in the PerfMeas package which is much better than the pr.curvefunction inPRROCpackage when the data is very large.
pr.curveis a nightmare and takes forever to finish when you have vectors with millions of entries.PerfMeastakes seconds in comparison.PRROCis written in R andPerfMeas` is written in C.