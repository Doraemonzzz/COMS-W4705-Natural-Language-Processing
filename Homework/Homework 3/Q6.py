# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:43:56 2020

@author: qinzhen
"""
import numpy as np
import pickle
from helper import *

f1 = "Q5_t.txt"
f2 = "Q5_q.txt"
with open(f1) as f:
    t = pickle.load(f)
    
with open(f2) as f:
    q = pickle.load(f)
    
#读取单词
en, vocab_en = process("scrambled.en", True)
de, vocab_de = process("original.de")

order = []

s1 = de[0]

INF = -1e10
eps = 1e-20

for s1 in de:
    m = len(s1)
    Log_prob = -1e100
    Index = 0
    for index, s2 in enumerate(en):
        #当前句子的对数分数
        log_prob = 0
        l = len(s2)
        for i in range(m):
            f = s1[i]
            #初始化
            score = INF
            alignment = 0
            #找到最优的alignment
            for a in range(l):
                k1 = (a, i, l, m)
                e = s2[a]
                if (k1 in q) and (e in t) and (f in t[e]):
                    s = np.log(q[k1] + eps) + np.log(t[e][f] + eps)
                    if s > score:
                        score = s
                        aligment = a
            #更新logprob
            log_prob += score
        if log_prob > Log_prob:
            Index = index
            Log_prob = log_prob
    
    order.append(Index)
    

#生成结果
scrambled = []
with open("scrambled.en") as f:
    for sentence in f.readlines():
        scrambled.append(sentence)
        

filename = "unscrambled.en"
with open(filename, "wb") as f:
    for index in order:
        f.writelines(scrambled[index])