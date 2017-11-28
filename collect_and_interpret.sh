#!/bin/sh

for dir in $(find test-data -type d); do
  ffmpeg -y -i $dir/audio.mp3 -ar 48000 -ac 1 $dir/audio.wav > /dev/null 2>&1
done
