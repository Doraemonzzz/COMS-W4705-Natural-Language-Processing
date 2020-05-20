# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:55:22 2020

@author: qinzhen
"""

import tagger_config
from subprocess import PIPE
import sys, subprocess

tags = tagger_config.tags

def sentence_reader(filename):
    sentences = []
    with open(filename) as f:
        sentence = [('*', '*')]
        sentence = []
        for word in f.readlines():
            w = word.strip().split()
            #非空
            if not w:
                sentences.append(sentence)
                sentence = [('*', '*')]
                sentence = []
            else:
                
                sentence.append(w)
            
    return sentences

def transform(sentence):
    res = ""
    n = len(sentence)
    for i in range(n):
        word = sentence[i]
        m = len(word)
        tmp = word[0]
        #单词之间以\t间隔
        for j in range(1, m):
            tmp += "\t" + word[j]
        res += tmp
        #除了最后一行增加换行
        if (i < n - 1):
             res += "\n"
        
    return res

def process(args):
    "Create a 'server' to send commands to."
    return subprocess.Popen(args, stdin=PIPE, stdout=PIPE)

def call(process, stdin):
    "Send command to a server and get stdout."
    res = []
    process.stdin.write(stdin + "\n\n")
    line = process.stdout.readline().strip()
    while line:
        res.append(line)
        line = process.stdout.readline().strip()
    return res
                            
def get_feature(sentence, his):
    #his=[i, tag[i-1], tag[i]]
    #BIGRAM
    BIGRAM = "BIGRAM:" + his[1] + ":" + his[2]
    #TAG
    i = int(his[0]) - 1
    TAG = "TAG:" + sentence[i][0] + ":" + his[2]
    
    return BIGRAM, TAG

def get_feature_v1(sentence, his):
    #his=[i, tag[i-1], tag[i]]
    res = []
    #BIGRAM
    BIGRAM = "BIGRAM:" + his[1] + ":" + his[2]
    if (his[1] == " "):
        print(his)
    res.append(BIGRAM)
    #TAG
    i = int(his[0]) - 1
    TAG = "TAG:" + sentence[i][0] + ":" + his[2]
    res.append(TAG)
    #SUFF
    for j in range(len(sentence)):
        word = sentence[j][0]
        n = len(word)
        for k in range(1, 4):
            if k <= n:
                tmp = "SUFF:" + word[-k:] + ":" + str(k) + ":" + his[2]
                res.append(tmp)
    
    return res