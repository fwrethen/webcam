#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys

from PIL import Image

video_filename = 'timelapse.mp4'
video_framerate = '6'
temp_folder = 'temp'

blacklist = ['cam_201806240020.jpg',
             'cam_201807260800.jpg',
             'cam_201807272000.jpg',
             'cam_201807261200.jpg',
             'cam_201808080800.jpg',
             'cam_201808141600.jpg',
             'cam_201808241800.jpg']

filter_regex = re.compile(r'^cam_(?!\d{8}(0[0-6]00|0004|2200))[0-9]+\.jpg$')

files = []

with os.scandir() as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_file():
            files.append(entry.name)

images = list(filter(filter_regex.search, files))
images = list(filter(lambda x: x not in blacklist, images))


if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

for cnt, image in enumerate(images):
    temp_img = temp_folder + '/' + image
    date = int(re.search(r'cam_(\d{8})', image).group(1))

    shutil.copyfile(image, temp_img)

    status_msg = "Cropping image {:3} of {}".format(cnt + 1, len(images))
    sys.stdout.write(status_msg)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(status_msg))

    crop1 = (415, 153, 1863, 968)
    crop2 = (415, 55, 1863, 870)
    if (date <= 20180726):
        crop = crop1
    else:
        crop = crop2

    im = Image.open(temp_img)
    im_cropped = im.crop(crop)
    im_cropped.save(temp_img, 'JPEG', quality=90)

sys.stdout.write("\n")

subprocess.call(['ffmpeg', '-y', '-r', video_framerate,
                 '-pattern_type', 'glob', '-i', temp_folder+'/cam_*.jpg',
                 '-s', 'hd720', '-vcodec', 'libx264', video_filename])

shutil.rmtree(temp_folder, ignore_errors=True)
