# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:26:03 2020

@author: qinzhen
"""

import pickle
from helper import *

#读取t
filename = "Q4_t.txt"
with open(filename) as f:
    t = pickle.load(f)

#读取单词
en, vocab_en = process("corpus.en", True)
de, vocab_de = process("corpus.de")

#获得计数
C1, C2, C3, C4 = get_count(en, de)

def delta2(t, q, k, i, j, lk, mk):
    e = en[k][j]
    f = de[k][i]
    s = 0
    for l in range(lk):
        e1 = en[k][l]
        s += t[e1][f] * q[(l, i, lk, mk)]
        
    return t[e][f] * q[(j, i, lk, mk)] / s

#训练
q = dict()
for key in C3:
    l = key[2]
    q[key] = 1.0 / l

S = 5
IBM_model(en, de, t, q, S, C1, C2, C3, C4, delta2, True)

#alignment
Alignment = []
for k in range(20):
    mk = len(de[k])
    lk = len(en[k])
    alignment = []
    for i in range(mk):
        f = de[k][i]
        p = 0
        a = 0
        for j in range(lk):
            e = en[k][j]
            if t[e][f] * q[(j, i, lk, mk)] > p:
                p = t[e][f] * q[(j, i, lk, mk)]
                a = j
        alignment.append(a)
    Alignment.append(alignment)

with open("Q5_aligment.txt", "w+") as f:
    for alignment in Alignment:
        f.write(" ".join(map(str, alignment)) + "\n")
        
#保存模型1的结果
with open("Q5_t.txt", "wb") as f:
    pickle.dump(t, f)
    
with open("Q5_q.txt", "wb") as f:
    pickle.dump(q, f)