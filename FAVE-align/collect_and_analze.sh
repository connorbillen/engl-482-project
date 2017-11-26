#!/bin/sh

# python3 pull-data/splib.py

for dir in $(find ../pull-data/test-data -type d); do
  # [ "$dir" == "pull-data/test-data" ] && continue 
  # ffmpeg -i $dir/audio.mp3 -ar 8000 -ac 1 $dir/audio.wav
  echo "$dir/audio.mp3"
  python FAAValign.py $dir/audio.wav $dir/english.txt 
done
