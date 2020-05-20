"""
This is an example of how to call the CL "servers" in python.
"""

from subprocess import PIPE
import sys, subprocess

def process(args):
  "Create a 'server' to send commands to."
  return subprocess.Popen(args, stdin=PIPE, stdout=PIPE)

def call(process, stdin):
  "Send command to a server and get stdout."
  output = process.stdin.write(stdin + "\n\n")
  line = ""
  while 1: 
    l = process.stdout.readline()
    if not l.strip(): break
    line += l
  return line

# Create a history server.
gold_server = process(
  ["python", "tagger_history_generator.py",  "GOLD"])

# Call with a sentence. 
gold_histories = call(gold_server, """There DET
is VERB 
no DET 
asbestos NOUN 
in ADP 
our PRON 
products NOUN 
now ADV 
. .""")
# Be careful, no end line.

print "First ", gold_histories

# Do it again.
gold_histories2 = call(gold_server, """There DET
is VERB 
no DET 
asbestos NOUN 
in ADP 
our PRON 
products NOUN 
now ADV 
. .""")

print "Second ", gold_histories2
