# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 14:59:44 2020

@author: qinzhen
"""
import pickle
from helper import process

#读取单词
en, vocab_en = process("corpus.en", True)
de, vocab_de = process("corpus.de")

#t存储概率，t1存储e对应的全体f
t = dict()
t1 = dict()
for e in vocab_en:
    t[e] = dict()
    #存储键
    t1[e] = set()

#迭代
for i, sentence in enumerate(en):
    for e in sentence:
        t1[e] = t1[e].union(set(de[i]))
        
for e in t:
    ne = len(t1[e])
    for f in t1[e]:
        t[e][f] = 1.0 / ne
        
filename = "data.txt"
with open(filename, "wb") as f:
    pickle.dump(t, f)