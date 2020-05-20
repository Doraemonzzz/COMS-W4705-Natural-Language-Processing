# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:05:10 2020

@author: qinzhen
"""

import pickle
from helper import *

#读取t
filename = "data.txt"
with open(filename) as f:
    t = pickle.load(f)

#读取单词
en, vocab_en = process("corpus.en", True)
de, vocab_de = process("corpus.de")

#获得计数
C1, C2, C3, C4 = get_count(en, de)

def delta1(t, q, k, i, j, lk, mk):
    e = en[k][j]
    f = de[k][i]
    s = 0
    for l in range(lk):
        e1 = en[k][l]
        s += t[e1][f]
        
    return t[e][f] / s

#训练
q = dict()
S = 5
IBM_model(en, de, t, q, S, C1, C2, C3, C4, delta1)

#保存结果
res = []
with open("devwords.txt") as f:
    for word in f.readlines():
        e = word.split()[0]
        f = list(t[e].keys())
        values = list(t[e].values())
        
        #排序
        data = zip(f, values)
        data.sort(key=lambda x: -x[1])
        #保存结果
        res.append([f[0] for f in data[:10]])

with open("Q4_word.txt", "w+") as f:
    for data in res:
        f.writelines(" ".join(data) + "\n")
        
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
            if t[e][f] > p:
                p = t[e][f]
                a = j
        alignment.append(a)
    Alignment.append(alignment)

with open("Q4_aligment.txt", "w+") as f:
    for alignment in Alignment:
        f.write(" ".join(map(str, alignment)) + "\n")
        
#保存模型1的结果
with open("Q4_t.txt", "wb") as f:
    pickle.dump(t, f)