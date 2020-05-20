#! /usr/bin/python

__author__="Alexander Rush <srush@csail.mit.edu>"
__date__ ="$Sep 12, 2012"

import sys, tagger_config

"""
A bigram global linear model decoder.
"""

class Scores:
  "Score manager for histories."
 
  def __init__(self, table, next):
    "Initialize the score table and the bigram transitions." 
    self.table = table
    t = ([p for p, a, b in self.table.iterkeys()])
    self.len = max(t) if t else 0
    self.next = next

  def length(self):
    return self.len

  def score(self, position, tag1, tag2):
    "Score the bigrams at a token position."
    key = (position, tag1, tag2)
    if key not in self.table:
      #print >>sys.stderr, "Not in table", key
      return -1e10
    return self.table[key]

  @staticmethod
  def score_reader(handle):
    "Read in the scores from stdin handle."
    scores = {}
    next = {} 
    while 1:
      line = sys.stdin.readline()
      if not line.strip():
        if scores == {}: break
        yield Scores(scores, next)
        scores = {}
        next = {}
      else:
        position, tag1, tag2, score = line.strip().split()
        scores[int(position), tag1, tag2] = float(score)
        next.setdefault((int(position), tag2), set())
        next[int(position), tag2].add(tag1)



def decode(scores):
  n = scores.length()
  K = tagger_config.tags + ["*", "STOP"]
  y = [""] * (n + 1)
  def q(k, u, v): return scores.score(k, u, v)
  def argmax(ls): return max(ls, key = lambda x: x[1])

  # The Viterbi algorithm.
  # Create and initialize the chart.
  pi = [((0, "*"), 1.0)] + \
      [((0, u), -1e10) for u in K if u != "*"]
  pi = dict(pi)
  bp = {}

  # Run the main loop. 
  for k in range(1, n + 1):
    for u in K:      
      if (k, u) not in scores.next: continue
      bp[k, u], pi[k, u]  = \
          argmax([(v, pi[k - 1, v] + q(k, v, u)) 
                  for v in scores.next[k, u]])  

  # Follow the back pointers in the chart.
  y[n], score  = argmax([(u, pi[n, u] + q(n + 1, u, "STOP")) 
                         for u in K if (n, u) in scores.next]) 
  for k in range(n - 1, 0, -1):
    y[k] = bp[k + 1, y[k + 1]]
  y[0] = "*"
  return y[1:n + 1], score

def usage(): 
  print """
  Usage: python tagger_decoder.py mode < scores
      Print the best scoring histories for a sentence.
"""

def main(mode):
  if mode == "HISTORY":
    for scores in Scores.score_reader(sys.stdin):
      if not scores: continue
      output = decode(scores)
      tags = ["*"] + output[0] + ["STOP"]
      for i in range(scores.length() + 1):
        j = i + 1
        print j, tags[j - 1], tags[j]
      print 
      sys.stdout.flush()

if __name__ == "__main__": 
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)
  main(sys.argv[1])
