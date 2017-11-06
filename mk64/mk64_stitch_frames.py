import glob
import hashlib
import os
import glob
import sys
import subprocess
from PIL import Image

# fetch list
f = open(sys.argv[1],'r')
    
def process_frame(frame_number):
    os.chdir("M:\\N64_360\\mk64\\images\\raw\\" + frame_number)
    
    print "Cropping"
    os.mkdir("M:\\N64_360\\mk64\\images\\raw\\" + frame_number + "\\crop")
    
    # Crop all images in this set
    for i in range(1,25):
      for j in range(0,2):
        img = Image.open(str(i) + "_" + str(j) + ".png")
        img = img.crop((4, 4, 1596, 1192))
        img.save("crop/" + str(i) + "_" + str(j) + ".png")
        
    img = Image.open("prev.png")
    img = img.crop((4, 4, 1596, 1192))
    img.save("crop/prev.png")
    img = Image.open("prev_1.png")
    img = img.crop((4, 4, 1596, 1192))
    img.save("crop/prev_1.png")
    
    os.chdir("M:\\N64_360\\mk64\\images\\raw\\" + frame_number + "\\crop\\")
    
    use_sub = [False]*25
    
    image_hashes = {}
    for i in range(1,25):
      image_hashes[str(i) + "_0"] = hashlib.md5(open(str(i) + "_0.png", 'rb').read()).digest()
      image_hashes[str(i) + "_1"] = hashlib.md5(open(str(i) + "_1.png", 'rb').read()).digest()
      
    prev_0_hash = hashlib.md5(open("prev.png", 'rb').read()).digest()
    prev_1_hash = hashlib.md5(open("prev_1.png", 'rb').read()).digest()
    
    prev_hashes = [prev_0_hash, prev_1_hash]
        
    for img in range(1,25):
      if (image_hashes[str(img) + "_0"] in prev_hashes):
        use_sub[img] = True
        print img
        
        if (image_hashes[str(img) + "_1"] in prev_hashes):
          print "ERROR"
          return
    
    img_list = []
    for img in range(1,25):
      if (use_sub[img]):
        img_list.append(str(img) + "_1.png")
      else:
        img_list.append(str(img) + "_0.png")
    
    os.chdir("M:\\N64_360\\mk64\\images\\raw\\" + frame_number)
    remap_command = ["c:\\Program Files\\Hugin\\bin\\nona.exe", "-o", "out", "-m", "TIFF_m", "..\\..\\..\\mk64_1600.pto"]
    print "Remapping"
    # Add the images to the command
    remap_command.extend(img_list)
    # Run the command and wait
    foo = subprocess.check_output(remap_command)
    print "Stitching"
    # Stitch process
    #excluding wrap
    #foo = subprocess.check_output(["c:\\Program Files\\Hugin\\bin\\enblend.exe", "-o", "M:\\N64_360\\mk64\\images\\" + x + ".tif", "out0000.tif", "out0001.tif", "out0002.tif", "out0003.tif", "out0004.tif", "out0005.tif", "out0006.tif", "out0007.tif", "out0008.tif", "out0009.tif", "out0010.tif", "out0011.tif", "out0012.tif", "out0013.tif", "out0014.tif", "out0015.tif", "out0016.tif", "out0017.tif", "out0018.tif", "out0019.tif", "out0020.tif", "out0021.tif", "out0022.tif", "out0023.tif"])
    
    # for tiff compression
    # --compression=deflate
    
    #include wrap, as png
    foo = subprocess.check_output(["c:\\Program Files\\Hugin\\bin\\enblend.exe", "--wrap", "-o", "M:\\N64_360\\mk64\\images\\" + x + ".png", "out0000.tif", "out0001.tif", "out0002.tif", "out0003.tif", "out0004.tif", "out0005.tif", "out0006.tif", "out0007.tif", "out0008.tif", "out0009.tif", "out0010.tif", "out0011.tif", "out0012.tif", "out0013.tif", "out0014.tif", "out0015.tif", "out0016.tif", "out0017.tif", "out0018.tif", "out0019.tif", "out0020.tif", "out0021.tif", "out0022.tif", "out0023.tif"])
    
    for filename in glob.glob("crop//*.png"):
      os.remove(filename)
    os.rmdir("M:\\N64_360\\mk64\\images\\raw\\" + frame_number + "\\crop")
    
    for filename in glob.glob("out*.tif"):
      os.remove(filename)
    
    print ""

    
while True:
    x = f.readline()
    x = x.rstrip()
    if not x: break
    print x
    process_frame(x)
