from PIL import Image, ImageDraw 
import os

parentdir = "/p/sdbb/ROSbot_data_collection/analysis/replay-output/"
imagefiles = os.listdir(parentdir)
images = []
imagefiles = sorted(imagefiles)
for imagefile in imagefiles:
    im = Image.open(parentdir + imagefile)
    images.append(im)
print(f"Total images: {len(images)}")
hz = 10
duration = int(1000 / hz)
print(f"GIF Duration: {duration}")
images[0].save(f"pillow_imagedraw_{hz}Hz.gif",
               save_all=True, 
               append_images=images[1:], 
               optimize=False, 
               duration=duration,  # each image in milliseconds
               loop=0)