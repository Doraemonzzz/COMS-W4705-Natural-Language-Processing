import sys

words = {}
word_count = {}
for l in sys.stdin:
  t = l.strip().split()
  if len(t) == 2:
    word_count.setdefault(t[0], 0)
    word_count[t[0]] += 1
    words.setdefault(t[0], set())
    words[t[0]].add(t[1])

dict = {}
for w, c in word_count.iteritems():
  if c >=5:
    dict[w] = list(words[w])

print dict
