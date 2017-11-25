#!/bin/sh

python3 pull-data/splib.py

for item in pull-data/test-data; do
  if [-d $item]; then
    python FAVE-align/FAAValign.py -v -i $item/english.txt $item/audio.mp3 $item/ipa.txt
  fi
done
