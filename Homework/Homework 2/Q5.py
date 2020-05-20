# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:38:20 2020

@author: qinzhen
"""

import json

#### Part 1 计算MLE
#计数
def Generate_count(File):
    Count_xyy = {}
    Count_xy = {}
    Count_x = {}
    Count_y = {}
    with open(File) as f:
        for i in f.readlines():
            #分隔数据
            data = i.strip().split()
            #判断
            if data[1] == "NONTERMINAL":
                Count_x[data[2]] = float(data[0])
            elif data[1] == "BINARYRULE":
                if data[2] not in Count_xyy:
                    Count_xyy[data[2]] = {}
                Count_xyy[data[2]][(data[3], data[4])] = float(data[0])
            else:
                if data[2] not in Count_xy:
                    Count_xy[data[2]] = {}
                Count_xy[data[2]][data[3]] = float(data[0])
                #统计单词数量
                if data[3] in Count_y:
                    Count_y[data[3]] += float(data[0])
                else:
                    Count_y[data[3]] = float(data[0])
                    
    return Count_xyy, Count_xy, Count_x, Count_y

def Generate_mle(Count_xyy, Count_xy, Count_x, Count_y):
    #计算MLE
    q_xyy = {}
    q_xy = {}
    for i in Count_x:
        q_xy[i] = {}
        q_xyy[i] = {}
        if i in Count_xy:
            for j in Count_xy[i]:
                q_xy[i][j] = Count_xy[i][j] / Count_x[i]
        if i in Count_xyy:
            for k in Count_xyy[i]:
                q_xyy[i][k] = Count_xyy[i][k] / Count_x[i]
                
    return q_xyy, q_xy

#### Part2: CKY
def CKY(word, Count_xyy, Count_xy, Count_x, Count_y, q_xyy, q_xy):
    n = len(word)
    Pi = {}
    Bp = {}
    for i in range(n):
        for j in range(i, n):
            Pi[(i, j)] = {}
            Bp[(i, j)] = {}
    
    for i in range(n):
        for x in Count_x:
            if x in Count_xy and word[i] in Count_xy[x]:
                Pi[(i, i)][x] = q_xy[x][word[i]]
                
    for l in range(1, n):
        for i in range(n - l):
            j = i + l
            for X in Count_x:
                #概率
                p = 0
                #最佳规则以及位置
                y1 = ""
                z1 = ""
                s1 = ""
                if X in q_xyy:
                    for (Y, Z) in q_xyy[X]:
                        for s in range(i, j):
                            if Y in Pi[(i, s)] and Z in Pi[(s + 1, j)]:
                                p1 = q_xyy[X][(Y, Z)] * Pi[(i, s)][Y] * Pi[(s + 1, j)][Z]
                                if p1 > p:
                                    p = p1
                                    y1 = Y
                                    z1 = Z
                                    s1 = s
                #更新最大值
                if p > 0:
                    Pi[(i, j)][X] = p
                    Bp[(i, j)][X] = (y1, z1, s1)
    
    pmax = 0
    node = ""
    if "S" in Pi[(0, n - 1)]:
        pmax = Pi[(0, n - 1)]["S"]
        node = "S"
    else:
        for i in Pi[(0, n - 1)]:
            if Pi[(0, n - 1)][i] > pmax:
                pmax = Pi[(0, n - 1)][i]
                node = i
    
    return Pi, Bp, node

#生成树
def tree(Bp, word, i, j, node):
    if j == i:
        return [node, word[i]]
    else:
        lnode, rnode, k = Bp[(i, j)][node]
        left = tree(Bp, word, i, k, lnode)
        right = tree(Bp, word, k + 1, j, rnode)
        return [node, left, right]

#生成结果
def Generate(File, output, Count_xyy, Count_xy, Count_x, Count_y, q_xyy, q_xy):
    Res = []
    with open(File) as f:
        for i in f.readlines():
            data = i.strip().split(" ")
            word = i.strip().split(" ")
            for j in range(len(data)):
                if data[j] not in Count_y or Count_y[data[j]] < 5:
                    data[j] = "_RARE_"
            
            #CKY算法
            Pi, Bp, node = CKY(data, Count_xyy, Count_xy, Count_x, Count_y, q_xyy, q_xy)
            n = len(word)
            #生成树
            res = tree(Bp, word, 0, n - 1, node)
            Res.append(res)
            
    with open(output, "w+") as f:
        for res in Res:
            r = json.dumps(res)
            f.write(r)
            f.write("\n")
            
#### 运行
File = "cfg_proc.counts"
f1 = "parse_dev.dat"
o1 = "parse_dev_result.dat"
Count_xyy, Count_xy, Count_x, Count_y = Generate_count(File)
q_xyy, q_xy = Generate_mle(Count_xyy, Count_xy, Count_x, Count_y)
Generate(f1, o1, Count_xyy, Count_xy, Count_x, Count_y, q_xyy, q_xy)

#检测结果
#python eval_parser.py parse_dev.key parse_dev_result.dat