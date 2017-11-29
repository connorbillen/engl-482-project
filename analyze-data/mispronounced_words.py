#!/usr/bin/python3

import os
import sys

english_words = open('../test-data/english.txt').read()
words = [] 
lengths = {} 

for speaker in os.listdir('../test-data/'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read() 
    except:
        print('transcription isn\'t there')
        continue

    transcription = transcription.split()
    for i in range(len(transcription)):
        if len(words) - 1 < i:
            words.append(set())

        words[i].add(transcription[i])

words = sorted(words, key=lambda word: len(word), reverse=True)
print("Top Five Words With Unique Pronunciations")
print(words[0:5])
