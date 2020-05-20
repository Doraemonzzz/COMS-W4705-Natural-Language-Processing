# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:28:30 2020

@author: qinzhen
"""
import json

#### Part 1 计数
def Count(File):
    Count_x = {}
    with open(File) as f:
        for i in f.readlines():
            #分隔数据
            data = i.split()
            #判断
            if data[1] == "UNARYRULE":
                #计算Count(x)
                if data[3] in Count_x:
                    Count_x[data[3]] += float(data[0])
                else:
                    Count_x[data[3]] = float(data[0])
    
    return Count_x

#### Part 2 处理低频词
def Replace_word(tree, Count_x):
    #基本情形
    if len(tree) == 2:
        word = tree[1]
        if word not in Count_x:
            tree[1] = "_RARE_"
        elif Count_x[word] < 5:
            tree[1] = "_RARE_"
    else:
        Replace_word(tree[1], Count_x)
        Replace_word(tree[2], Count_x)

#### Part 3 换并输出
def Replace(File, output, Count_x):
    Res = []
    with open(File) as f:
        for i in f.readlines():
            tree = json.loads(i, encoding="utf-8")
            Replace_word(tree, Count_x)
            res = json.dumps(tree)
            Res.append(res)
            
    with open(output, "w+") as f:
        for i in Res:
            f.write(i)
            f.write("\n")
            
def Replace_dev(File, output, Count_x):
    Res = []
    with open(File) as f:
        for i in f.readlines():
            data = i.strip().split(" ")
            for j in range(len(data)):
                if data[j] not in Count_x or Count_x[data[j]] < 5:
                    data[j] = "_RARE_"
            Res.append(" ".join(data) + "\n")
    
    with open(output, "w+") as f:
        for i in Res:
            f.writelines(i)

#### 运行
File = "cfg.counts"
Count_x = Count(File)

#训练数据
f1 = "parse_train.dat"
o1 = "parse_train_proc.dat"
Replace(f1, o1, Count_x)

#测试数据
f2 = "parse_dev.dat"
o2 = "parse_dev_proc.dat"
Replace_dev(f2, o2, Count_x)

#python count_cfg_freq.py parse_train_proc.dat > cfg_proc.counts