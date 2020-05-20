# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:05:30 2019

@author: qinzhen
"""

import numpy as np

# =============================================================================
# Q5
# =============================================================================
#### Part 1 计算MLE
File = "ner_proc.counts"
q2 = {}
q3 = {}
with open(File) as f:
    for i in f.readlines():
        #分隔数据
        data = i.split()
        #判断
        if data[1] == "2-GRAM":
            q2[(data[2], data[3])] = float(data[0])
            q3[(data[2], data[3])] = {}
        elif data[1] == "3-GRAM":
            q3[(data[2], data[3])][(data[2], data[3], data[4])] = float(data[0])

#计算 MLE
q = {}
for i in q3:
    for j in q3[i]:
        q[j] = q3[i][j] / q2[i]
'''
#计算对数概率
for j in q:
    res = ' '.join(j) + " : " + str(math.log(q[j]))
    print(res)
    
'''
 
#### Part 2
def Viterbi(sentence, q, e):
    #K_0 = *
    #标签数量
    K = list(Count_y.keys())
    #动态规划表
    Pi = {}
    #反向指针表
    bp = {}
    #单词数量
    n = len(sentence)
    for i in range(n + 1):
        Pi[i-1] = {}
        bp[i-1] = {}
    #初始化
    Pi[-1][("*", "*")] = 1
    #遍历句子中的单词
    for k in range(n):
        #可以选的标签
        K0 = K
        K1 = K
        K2 = K
        if k == 0:
            K0 = ["*"]
            K1 = ["*"]
        elif k == 1:
            K0 = ["*"]
        '''
        elif k == n-1:
            K2 = K + ["STOP"]
        '''
        
        #循环
        for u in K1:
            for v in K2:
                p = 0
                w_arg = ""
                key = sentence[k]
                if key not in Count_x or Count_x[key] < 5:
                    key = "_RARE_"
                for w in K0:
                    if (w, u) in Pi[k-1] and (w, u, v) in q and (v, key) in e[key]:
                        p1 = Pi[k-1][(w, u)] * q[(w, u, v)] * e[key][(v, key)]
                        if p1 > p:
                            p = p1
                            w_arg = w
                Pi[k][(u, v)] = p
                bp[k][(u, v)] = w_arg
    
    #计算最后两个标签
    y0 = ""
    y1 = ""
    pmax = 0
    for u in K:
        for v in K:
            if (u, v) in Pi[n-1] and (u, v, "STOP") in q:
                p = Pi[n-1][(u, v)] * q[(u, v, "STOP")]
                if p > pmax:
                    pmax = p
                    y0 = u
                    y1 = v
    
    tag = [y1, y0]
    
    for k in range(n-3, -1, -1):
        y = bp[k+2][(y0, y1)]
        tag.append(y)
        #更新
        y1 = y0
        y0 = y
    
    #反序
    tag = tag[::-1][2:]
    
    return tag, pmax

res_viterbi = []
for sentence in Sentence:
    #print(sentence)
    tag, p = Viterbi(sentence, q, e_proc)
    res_viterbi.append(" ".join(tag) + " " + str(p) + "\n")



#产生结果    
File = "ner_dev_viterbi.dat"
with open(File, "w+") as f:
    for i in res:
        f.writelines(i)