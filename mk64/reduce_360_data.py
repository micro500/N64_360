import sys
import math

with open(sys.argv[2]) as f:
    frame_list = [x.strip() for x in f.readlines()] 

data = open(sys.argv[1],'r')
    
while True:
    x = data.readline()
    x = x.rstrip()
    if not x: break
    parts = x.split(",")
    
    if (parts[0] in frame_list):
      print x
      