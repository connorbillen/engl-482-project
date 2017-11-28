#!/bin/sh

for dir in $(find test-data -type d); do
  python3 analyze-data/FAVEToTxt.py $dir/audio.TextGrid $dir/audio_arpabet.txt
done
