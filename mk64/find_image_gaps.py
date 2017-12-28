import glob
import hashlib
import os
import glob
import sys
import subprocess

# fetch list
f = open(sys.argv[1],'r')
prev_frame = -1
while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    
    x = int(x)
    
    if (prev_frame != -2):
      delta = x - prev_frame
      #if (delta != 2):
      if (delta == 3 or delta == 1):
        print str(prev_frame) + " -> " + str(x) + " (" + str(delta) + ")"
      
    prev_frame = x
    