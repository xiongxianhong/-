#coding:gbk
"""
目的:基于Python和Gelphi的《黎明破晓的街道》人物关系图谱构建
作者:熊先红
2020/1/3
"""

import os,sys
import jieba,codecs,math
import jieba.posseg as pseg

names={}
relationships={}
linenames=[]

jieba.load_userdict("dict.txt")  #新建一个dict文档提取字典
with codecs.open("黎明破晓的街道.txt","r","gbk") as rng:
	for line in rng.readlines():
		poss=pseg.cut(line)
		linenames.append([])
		for w in poss:
			if w.flag != "nr" or len(w.word)<2:
				continue
			linenames[-1].append(w.word)
			if names.get(w.word) is None:
				names[w.word]=0
				relationships[w.word]={}
			names[w.word] += 1
			
for line in linenames:  #使用for循环提取每个人物和角色名
	for name1 in line:
		for name2 in line:
			if name1 == name2:
				continue
			if relationships[name1].get(name2) is None:
				relationships[name1][name2]=1
			else:
				relationships[name1][name2]=relationships[name1][name2]+1
				
with codecs.open("node.txt","w","gbk") as rng:  #新建两个文档，将角色名按行显示
	rng.write("Id Label Weight\r\n")
	for name,times in names.items():
		rng.write(name+" "+name+" "+str(times)+"\r\n")
		
with codecs.open("edge.txt","w","gbk") as rng:
	rng.write("Source Target Weight\r\n")
	for name,edges in relationships.items():
		for v,w in edges.items():
			if w>10:
				rng.write(name+" "+v+" "+str(w)+"\r\n")
