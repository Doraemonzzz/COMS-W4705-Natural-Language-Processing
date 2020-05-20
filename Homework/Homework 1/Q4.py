# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:07:14 2019

@author: qinzhen
"""

import numpy as np

#python count_freqs.py ner_train_proc.dat > ner_proc.counts

# =============================================================================
# Q4
# =============================================================================
#### Part 1 计算MLE
File = "ner.counts"
Count_x_y = {}
Count_y = {}
Count_x = {}
with open(File) as f:
    for i in f.readlines():
        #分隔数据
        data = i.split()
        #判断
        if data[1] == "WORDTAG":
            #计算Count(y, x)
            Count_x_y[(data[2], data[3])] = float(data[0])
            #计算Count(y)
            if data[2] in Count_y:
                Count_y[data[2]] += float(data[0])
            else:
                Count_y[data[2]] = float(data[0])
            #计算Count(x)
            if data[3] in Count_x:
                Count_x[data[3]] += float(data[0])
            else:
                Count_x[data[3]] = float(data[0])

e = {}
for i in Count_x_y:
    e[i] = Count_x_y[i] / Count_y[i[0]]

#### Part 2 处理低频词
File = "ner_train.dat"
res = []
with open(File) as f:
    for i in f.readlines():
        #分隔数据
        data = i.split()
        if len(data) > 0:
            #判断次数
            if Count_x[data[0]] < 5:
                data[0] = "_RARE_"
                content = ' '.join(data) + "\n"
                i = content
        res.append(i)

#生成文件
File = "ner_train_proc.dat"
with open(File, "w+") as f:
    for i in res:
        f.writelines(i)
 
#### Part 3 重新计算MLE
File = "ner_proc.counts"
Count_x_y_proc = {}
Count_y_proc = {}
Count_x_proc = {}
with open(File) as f:
    for i in f.readlines():
        #分隔数据
        data = i.split()
        #判断
        if data[1] == "WORDTAG":
            #计算Count(y, x)
            Count_x_y_proc[(data[2], data[3])] = float(data[0])
            #计算Count(y)
            if data[2] in Count_y_proc:
                Count_y_proc[data[2]] += float(data[0])
            else:
                Count_y_proc[data[2]] = float(data[0])
            #计算Count(x)
            if data[3] in Count_x_proc:
                Count_x_proc[data[3]] += float(data[0])
            else:
                Count_x_proc[data[3]] = float(data[0])

#### Part 4 计算argmax(e(x|y))
                
#按单词生成字典，每个字典元素为字典
e_proc = {}
for i in Count_x_proc:
    e_proc[i] = {}

for i in Count_x_y_proc:
    e_proc[i[1]][i] = Count_x_y_proc[i] / Count_y_proc[i[0]]


#生成结果
File = "ner_dev.dat"
res = []
#验证数据的句子
Sentence = []
s = []
with open(File) as f:
    for i in f.readlines():
        #分隔数据
        data = i.split()
        #记录句子
        if len(data) > 0:
            key = data[0]
            #判断是否为低频词
            if key not in Count_x or Count_x[key] < 5:
                key = "_RARE_"
            #找到argmax(e(x|y))
            p = 0
            label = ""
            for j in e_proc[key]:
                p1 = e_proc[key][j]
                if p1 > p:
                    p = p1
                    label = j[0]
                #生成结果
                i = ' '.join([data[0], label, str(p)]) + "\n"
            s += data
        else:
            Sentence.append(s)
            s = []
        res.append(i)

#产生结果    
File = "ner_dev_proc.dat"
with open(File, "w+") as f:
    for i in res:
        f.writelines(i)

#测试结果
#python eval_ne_tagger.py ner_dev.key ner_dev_proc.dat
      
# =============================================================================
# Q5
# =============================================================================
#### Part 1 计算MLE
#预处理
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
 
#### Part 2 维特比算法
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
       
    #判断长度是否为1
    if n == 1:
        y = ""
        pmax = 0
        for u in K + ["*"]:
            for v in K + ["*"]:
                if (u, v) in Pi[n-1] and (u, v, "STOP") in q:
                    p = Pi[n-1][(u, v)] * q[(u, v, "STOP")]
                    if p > pmax:
                        pmax = p
                        y = v
        tag = [y]
    else:
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
        tag = tag[::-1]
    
    return tag, pmax

#### Part 3 产生结果
Res_viterbi = []
P = []

#产生结果    
File = "ner_dev_viterbi.dat"
with open(File, "w+") as f:
    for sentence in Sentence:
        #print(sentence)
        tag, p = Viterbi(sentence, q, e_proc)
        if(p == 0):
            print(sentence)
            break
        logp = np.log(p)
        Res_viterbi.append(tag)
        P.append(p)
        for i in range(len(sentence)):
            data = ' '.join([sentence[i], tag[i], str(logp)]) + "\n"
            f.writelines(data)
        #换行符
        f.writelines("\n")
        
#python eval_ne_tagger.py ner_dev.key ner_dev_viterbi.dat





'''
sentence = Sentence[0]

sentence = ['Their', 'stay', 'on', 'top', ',', 'though', ',', 'may', 'be', 'short-lived', 'as', 'title', 'rivals', 'Essex', ',', 'Derbyshire', 'and', 'Surrey', 'all', 'closed', 'in', 'on', 'victory', 'while', 'Kent', 'made', 'up', 'for', 'lost', 'time', 'in', 'their', 'rain-affected', 'match', 'against', 'Nottinghamshire', '.']
sentence = ["May"]
sentence = ['--', 'Dhaka', 'Newsroom', '880-2-506363']
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
    #循环
    for u in K1:
        for v in K2:
            p = 0
            w_arg = ""
            key = sentence[k]
            if key not in Count_x or Count_x[key] < 5:
                key = "_RARE_"
            for w in K0:
                if (w, u) in Pi[k-1] and (w, u, v) in q and (v, key) in e_proc[key]:
                    p1 = Pi[k-1][(w, u)] * q[(w, u, v)] * e_proc[key][(v, key)]
                    if p1 > p:
                        p = p1
                        w_arg = w
            if p > 0:
                Pi[k][(u, v)] = p
                bp[k][(u, v)] = w_arg

#判断长度是否为1
if n == 1:
    y = ""
    pmax = 0
    for u in K + ["*"]:
        for v in K + ["*"]:
            if (u, v) in Pi[n-1] and (u, v, "STOP") in q:
                p = Pi[n-1][(u, v)] * q[(u, v, "STOP")]
                if p > pmax:
                    pmax = p
                    y = v
    tag = [y]
else:
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
'''
