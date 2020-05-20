#! /usr/bin/python

__author__="Alexander Rush <srush@csail.mit.edu>"
__date__ ="$Sep 12, 2012"

import sys, re, json, itertools

"""
Evaluate a set of test parses versus the gold set. 
"""

def simplify_non_terminal(nt):
  "Remove the vertical markovization." 
  return re.sub(r"\^<.*?>", '', nt)


def convert_to_spans(tree, start, set): 
  "Convert a tree into spans (X, i, j) and add to a set." 
  if len(tree) == 3:
    # Binary Rule.
    split = convert_to_spans(tree[1], start, set)
    end = convert_to_spans(tree[2], split + 1, set)
    set.add((simplify_non_terminal(tree[0]), start, end))
    return end
  elif len(tree) == 2:
    # Unary Rule.
    set.add((simplify_non_terminal(tree[0]), start, start))
    return start

def output_header():
  print "%10s  %10s  %10s  %10s   %10s"%("Type", "Total", "Precision", "Recall", "F1 Score")
  print "==============================================================="

def output_row(name, right, total_gold, total_test):
  p = right / float(total_test)
  r = right / float(total_gold)
  print "%10s        %4d     %0.3f        %0.3f        %0.3f"%(name, total_gold, p, r, (2 * p * r) / float(p + r))

def main(key_file, prediction_file):
  right = 0
  total_gold = 0
  total_test = 0
  nt_right = {}
  nt_total_gold = {}
  nt_total_test = {}

  for l1, l2 in itertools.izip(open(key_file), open(prediction_file)):
    set1 = set()
    set2 = set()
    tree1 = json.loads(l1)
    tree2 = json.loads(l2)
    len1 = convert_to_spans(tree1, 1, set1)
    len2 = convert_to_spans(tree2, 1, set2)
    if len1 != len2: 
      print >>sys.stderr, "Sentence length does not match", l1, l2 
    
    # Compute precision, recall.
    for (nt, i, j) in set1 & set2:
      nt_right.setdefault(nt, 0)
      nt_right[nt] += 1

    for (nt, i, j) in set1:
      nt_total_gold.setdefault(nt, 0)
      nt_total_gold[nt] += 1

    for (nt, i, j) in set2:
      nt_total_test.setdefault(nt, 0)
      nt_total_test[nt] += 1
      
    total_gold += len(set1)
    total_test += len(set2)
    right += len(set1 & set2)
  output_header()
  N = nt_right.keys()
  N.sort()
  for nt in N:
    output_row(nt, nt_right[nt], 
               nt_total_gold.get(nt, 0), 
               nt_total_test.get(nt, 0))
  print
  output_row("total", right, total_gold, total_test)
    

def usage():
    sys.stderr.write("""
    Usage: python eval_parser.py [key_file] [output_file]
        Evalute the accuracy of a output trees compared to a key file.\n""")

if __name__ == "__main__": 
  if len(sys.argv) != 3:
    usage()
    sys.exit(1)
  main(sys.argv[1], sys.argv[2]) 


