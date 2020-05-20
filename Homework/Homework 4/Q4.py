# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:33:38 2020

@author: qinzhen
"""
from helper import *

#读取
def get_value(filename):
    value = dict()
    
    with open(filename) as f:
        for string in f.readlines():
            fea, v = string.strip().split()
            value[fea] = float(v)
    
    return value

def generate(output, sentences, F):
    with open(output, "wb") as f:
        for sentence in sentences:
            sent = transform(sentence)
            history = call(enum_server, sent)
            score_ = []
            for his in history:
                score = 0
                feature = F(sentence, his.split())
                for fea in feature:
                    if fea in value:
                        score += value[fea]
                score_.append(his + "\t" + str(score))
            score_ = '\n'.join(score_)
            #生成结果
            res = call(decoder_server, score_)
            #保存
            n = len(sentence)
            for i in range(n):
                tmp = sentence[i][0] + "\t" + res[i].split()[-1]
                f.writelines(tmp)
                f.write("\n")
            f.write("\n")

enum_server = process(["python", "tagger_history_generator.py", "ENUM"])
decoder_server = process(["python", "tagger_decoder.py", "HISTORY"])
filename = "tag_dev.dat"
sentences = sentence_reader(filename)

#Q4
f1 = "tag.model"
o1 = "Q4.out"
value = get_value(f1)
generate(o1, sentences, get_feature)
#python eval_tagger.py tag_dev.key Q4.out

#Q5
f2 = "Q5.model"
o2 = "Q5.out"
value = get_value(f2)
generate(o2, sentences, get_feature_v1)
#python eval_tagger.py tag_dev.key Q5.out