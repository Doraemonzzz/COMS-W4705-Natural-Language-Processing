# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:09:13 2020

@author: qinzhen
"""
import copy
NULL = "NULL"

def process(filename, flag=False):
    data = []
    vocab = []
    with open(filename) as f:
        for sentence in f.readlines():
            word = sentence.split()
            if flag:
                word = [NULL] + word
            data.append(word)
            vocab += word
    return data, set(vocab)

def get_count(en, de):
    #生成计数
    C1 = dict()
    C2 = dict()
    C3 = dict()
    C4 = dict()
    n = len(en)
    
    for k in range(n):
        mk = len(de[k])
        #包括NULL
        lk = len(en[k])
        for i in range(mk):
            for j in range(lk):
                e = en[k][j]
                f = de[k][i]
                C1[(e, f)] = 0
                C2[e] = 0
                C3[(j, i, lk, mk)] = 0
                C4[(i, lk, mk)] = 0
                
    return C1, C2, C3, C4

#IBM模型
def IBM_model(en, de, t, q, S, C1, C2, C3, C4, delta, flag=False):
    n = len(en)
    for s in range(S):
        c1 = copy.deepcopy(C1)
        c2 = copy.deepcopy(C2)
        c3 = copy.deepcopy(C3)
        c4 = copy.deepcopy(C4)
        for k in range(n):
            mk = len(de[k])
            #包括NULL
            lk = len(en[k])
            for i in range(mk):
                for j in range(lk):
                    e = en[k][j]
                    f = de[k][i]
                    #计算delta
                    d = delta(t, q, k, i, j, lk, mk)
                    #更新
                    c1[(e, f)] += d
                    c2[e] += d
                    c3[(j, i, lk, mk)] += d
                    c4[(i, lk, mk)] += d
        
        #更新t
        for e in t:
            for f in t[e]:
                t[e][f] = c1[(e, f)] / c2[e]
        
        #更新q
        if flag:
            for k1 in C3:
                k2 = k1[1:]
                q[k1] = c3[k1] / c4[k2]