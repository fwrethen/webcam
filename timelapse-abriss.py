#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

video_filename = 'timelapse.mp4'
video_framerate = '24'
video_crf = '23'
caption_date = True
temp_folder = 'temp'

blacklist = []

filter_regex = re.compile(r'^cam_\d{12}\.jpg$')
date_filter = [
    '20191028',
    '20191029',
    '20191030',
    '20191104',
    '20191105',
    '20191106',
    '20191107',
    '20191108',
    '20191111',
    '20191112',
    '20191113',
    '20191114',
    '20191115',
    '20191118',
    '20191119',
    '20191120',
    '20191121',
    '20191122',
    '20191125',
    '20191126',
    '20191127',
    '20191128',
    '20191129',
]

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
    if date not in date_filter:
        continue
    if (int(time) < 700 or int(time) > 1700) and (time.endswith('5') or int(time[-2]) % 2 != 0):
        continue


    status_msg = "Processing image {:3} of {}".format(cnt + 1, len(images))
    sys.stdout.write(status_msg)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(status_msg))

    crop = (415, 55, 1863, 870)

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
