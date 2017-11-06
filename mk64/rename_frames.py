import glob
import hashlib
import os
import glob
import sys
import subprocess

# fetch list
f = open(sys.argv[1],'r')
   
while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    print x

    x_i = int(x)
    x_i = x_i + 1
    
    foo = subprocess.check_output(["mv", x + ".png", "final//" + str(x_i) + ".png"])
    