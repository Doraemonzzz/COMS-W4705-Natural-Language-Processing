#! /usr/bin/python

__author__="Alexander Rush <srush@csail.mit.edu>"
__date__ ="$Sep 12, 2012"

import sys, tagger_config

"""
Output the histories for a sentence. 
"""

tags = tagger_config.tags

def sent_reader(handle):
  words = []
  while 1:
    line = sys.stdin.readline()
    if not line.strip():
      if words != []:
        yield [("*", "*")] + words
        words = []
      else: 
        return
    else:
      words.append(line.strip().split())
  yield [("*", "*")] + words

def main(mode):
  for sentence in sent_reader(sys.stdin):
    if mode == "GOLD":
      for i, (word, tag) in enumerate(sentence):
        if i == 0: continue
        print "%d %5s %5s"%(i, sentence[i - 1][1], tag)
    if mode == "ENUM":
      for i in range(len(sentence)):
        word = sentence[i][0]
        if i == 0: continue
        if i == 1: 
          tagset = tagger_config.dict.get(word, tags)
          for t2 in tagset:
            print "%d %5s %5s"%(i, "*", t2)
        else:
          last_word = sentence[i - 1][0]
          tagset = tagger_config.dict.get(word, tags)
          last_tagset = tagger_config.dict.get(last_word, tags)
          for t1 in last_tagset:
            for t2 in tagset:
              print "%d %5s %5s"%(i, t1, t2)
    print
    sys.stdout.flush()
def usage(): 
  print """
  Usage: python tagger_history_generator.py mode
      Print the histories for a sentence.
"""

if __name__ == "__main__": 
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)
  main(sys.argv[1])

