import sys
import math

f = open(sys.argv[1],'r')
last_parts = []
while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    parts = x.split(",")

    if (not last_parts):
        last_parts = parts
    else:
        parts_match = True
        for i in range(1, 13):
            if (parts[i] != last_parts[i]):
                parts_match = False
                break
        if (not parts_match):
            start_frame = int(last_parts[0]) #-1
            end_frame = int(parts[0]) #-1
            
            # Comment on non 30fps instances
            if ((end_frame - start_frame) != 2):
              print last_parts[0] + " -> " + parts[0] + "(" + str((end_frame - start_frame)) + ")"
              
            print end_frame
            
            last_parts = parts
