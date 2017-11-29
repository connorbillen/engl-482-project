#!/usr/bin/python3

import os
import sys
from MapDrawer import MapDrawer

md = MapDrawer('Test Map')
english_words = open('../test-data/english.txt').read()
words = [] 
lengths = {} 

for speaker in os.listdir('../test-data/'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read() 
    except:
        continue

    try:
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        md.add_points(latitude, longitude)
    except:
        print('No lat/long data for Speaker ', speaker)
        continue


    transcription = transcription.split()
    for i in range(len(transcription)):
        if len(words) - 1 < i:
            words.append(set())

        words[i].add(transcription[i])

words = sorted(words, key=lambda word: len(word), reverse=True)
print("Top Five Words With Unique Pronunciations")
print(words[0:5])

md.draw()
