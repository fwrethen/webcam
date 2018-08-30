#!/bin/bash

BLACKLIST=(cam_201806240020.jpg cam_201807260800.jpg cam_201807272000.jpg cam_201807261200.jpg cam_201808080800.jpg cam_201808141600.jpg cam_201808241800.jpg)

mkdir temp
ls | grep '^cam_[0-9]\+\.jpg$' | grep -v -e '0[0-6]00.jpg' -e '0004.jpg' -e '2200.jpg' | grep -v ${BLACKLIST[@]/#/-e } | xargs cp -t temp/

ffmpeg -y -r 6 -pattern_type glob -i 'temp/cam_*.jpg' -s hd720 -vcodec libx264 timelapse.mp4

rm -r temp
