import glob
import hashlib
import os
import glob
import sys
import subprocess
import time
from PIL import Image

# fetch list
f = open(sys.argv[1],'r')
    
def process_frame(frame_number):
    os.chdir("M:\\N64_360\\mk64\\images\\raw\\pre")
    
    print "Remapping"
    remap_command = ["c:\\Program Files\\Hugin\\bin\\nona.exe", "-o", "out", "-m", "TIFF_m", "..\\..\\..\\mk64_pre.pto"]
    # Add the images to the command
    remap_command.extend([frame_number + ".png"])
    # Run the command and wait
    foo = subprocess.check_output(remap_command, stderr=subprocess.STDOUT)

    print "Stitching"
    # Stitch process
    #excluding wrap
    #foo = subprocess.check_output(["c:\\Program Files\\Hugin\\bin\\enblend.exe", "-o", "M:\\N64_360\\mk64\\images\\" + x + ".tif", "out0000.tif", "out0001.tif", "out0002.tif", "out0003.tif", "out0004.tif", "out0005.tif", "out0006.tif", "out0007.tif", "out0008.tif", "out0009.tif", "out0010.tif", "out0011.tif", "out0012.tif", "out0013.tif", "out0014.tif", "out0015.tif", "out0016.tif", "out0017.tif", "out0018.tif", "out0019.tif", "out0020.tif", "out0021.tif", "out0022.tif", "out0023.tif"])
    
    # for tiff compression
    # --compression=deflate
    
    #include wrap, as png
    foo = subprocess.check_output(["c:\\Program Files\\Hugin\\bin\\enblend.exe", "--wrap", "-f", "8192x4096", "-o", "M:\\N64_360\\mk64\\images\\raw\\pre\\temp\\" + frame_number + ".png", "out0000.tif"])
    
    print "Adding black"
    img = Image.open("M:\\N64_360\\mk64\\images\\raw\\pre\\temp\\" + frame_number + ".png", 'r')
    background = Image.new('RGBA', (8192, 4096), (0, 0, 0, 255))
    background.paste(img, (0,0), img)
    background.save("M:\\N64_360\\mk64\\images\\raw\\pre\\final\\" + frame_number + ".png")
    
    print "Cleanup"
    os.remove("out0000.tif")
    os.remove("M:\\N64_360\\mk64\\images\\raw\\pre\\temp\\" + frame_number + ".png")
    

total_time = 0
frame_count = 0

while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    print x
    
    start = time.time()
    process_frame(x)
    end = time.time()

    delta_time = end - start
    total_time = total_time + delta_time
    
    frame_count = frame_count + 1
    average_time = total_time / frame_count
    
    print str(delta_time) + "s, average of " + str(frame_count) + ": " + str(average_time)
    print ""