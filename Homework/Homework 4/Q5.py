# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:17:34 2020

@author: qinzhen
"""

#参考https://github.com/huxiuhan/nlp-hw

from helper import *

filename = "tag.model"
value = dict()

enum_server = process(["python", "tagger_history_generator.py", "ENUM"])
gold_server = process(["python", "tagger_history_generator.py", "GOLD"])
decoder_server = process(["python", "tagger_decoder.py", "HISTORY"])

filename = "tag_train.dat"
sentences = sentence_reader(filename)

K = 5
#历史
History = []
History_label = []
for sentence in sentences:
    sent = transform(sentence)
    history = call(enum_server, sent)
    history_label = call(gold_server, sent)
    History.append(history)
    History_label.append(history_label)
N = len(sentences)

#训练
for k in range(K):
    for i, sentence in enumerate(sentences):
        sent = transform(sentence)
        history = History[i]
        #真实结果
        history_label = History_label[i]
        score_ = []
        for his in history:
            score = 0
            feature = get_feature_v1(sentence, his.split())
            for fea in feature:
                if fea in value:
                    score += value[fea]
            score_.append(his + "\t" + str(score))
        score_ = '\n'.join(score_)
        #生成结果
        res = call(decoder_server, score_)
        #比较结果
        flag = True
        n = len(history_label)
        
        for j in range(n):
            a1 = res[j][-1]
            a2 = history_label[j].split()[-1]
            if a1 != a2:
                #不相同
                for f in get_feature_v1(sentence, res[j].split()):
                    if f in value:
                        value[f] -= 1
                    else:
                        value[f] = -1
                #相同
                for f in get_feature_v1(sentence, history_label[j].split()):
                    if f in value:
                        value[f] += 1
                    else:
                        value[f] = 1

#生成结果
outputname = "Q5.model"
with open(outputname, "wb") as f:
    for fea in value:
        f.writelines(fea + " " + str(value[fea]))    
        f.writelines("\n")