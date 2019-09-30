#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

video_filename = 'timelapse.mp4'
video_framerate = '6'
video_crf = '30'
caption_date = True
temp_folder = 'temp'

blacklist = ['cam_201806240020.jpg',
             'cam_201807260800.jpg',
             'cam_201807272000.jpg',
             'cam_201807261200.jpg',
             'cam_201808080800.jpg',
             'cam_201808141600.jpg',
             'cam_201808241800.jpg',
             'cam_201810020800.jpg',
             'cam_201812060800.jpg',
             'cam_201812090800.jpg',
             'cam_201901260800.jpg']

filter_regex = re.compile(r'^cam_\d{12}\.jpg$')

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
    date, time = re.search(r'cam_(\d{8})(\d{4})', image).group(1, 2)

    status_msg = "Processing image {:3} of {}".format(cnt + 1, len(images))
    sys.stdout.write(status_msg)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(status_msg))

    # Do not process images taken at night.
    if ((22 <= int(time) <= 600) or (int(time) >= 2100) or
            (int(date) > 20180910 and int(time) > 1900) or
            (int(date) > 20181027 and int(time) > 1700) or
            (int(date) > 20181212 and int(date) < 20190117 and int(time) < 900) or
            (int(time) <= 4)):
        continue

    crop1 = (415, 153, 1863, 968)
    crop2 = (415, 55, 1863, 870)
    if (int(date) <= 20180726):
        crop = crop1
    else:
        crop = crop2

    im = Image.open(image)
    im_cropped = im.crop(crop)

    if caption_date:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
            36,
            encoding="unic"
        )
        draw = ImageDraw.Draw(im_cropped)
        date = '.'.join(map(str, (date[-2:], date[-4:-2], date[:4])))
        margin = 40
        width, height = im_cropped.size
        textwidth, textheight = draw.textsize(date, font)
        xy = (width - textwidth - margin, height - textheight - margin)
        draw.text(xy, date, font=font, fill=(96, 96, 96))

    im_cropped.save(temp_folder + '/' + image, 'JPEG', quality=90)

sys.stdout.write("\n")

subprocess.call(['ffmpeg', '-y', '-r', video_framerate,
                 '-pattern_type', 'glob', '-i', temp_folder + '/cam_*.jpg',
                 '-s', 'hd720', '-vcodec', 'libx264', '-crf', video_crf, video_filename])

shutil.rmtree(temp_folder, ignore_errors=True)
