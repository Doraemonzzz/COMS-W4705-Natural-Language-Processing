from itertools import *
import sys

def main(file1, file2):
  right = 0
  total = 0
  for l1, l2 in izip(open(file1), open(file2)):
    total += 1
    if l1 == l2:
      right += 1 
  print "Right\tTotal\tAcc"
  print "%d\t%d\t%0.3f"%(right, total, right / float(total))

if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
  
