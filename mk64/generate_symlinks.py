import glob
import hashlib
import os
import glob
import sys
import subprocess

# fetch list
f = open(sys.argv[1],'r')

counter = 1
    
last_x = -1
while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    print x

    needed = 1
    if (last_x != -1):
      needed = int(x) - last_x      
      
    for i in range(0, needed):
      foo = subprocess.check_output(["ln", "-s", "//media//sf_N64_360//mk64//images//final//" + x + ".png", "{0:05d}.png".format(counter)])
      
      counter = counter + 1
      
    last_x = int(x)
    
    

    

