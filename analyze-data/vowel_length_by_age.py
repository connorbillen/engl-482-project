#!/usr/bin/python3

import os
import sys
import pickle
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class Speaker:
    def __init__(self, lat, lon, words, male, age):
        self.lat = lat
        self.lon = lon
        self.words = words
        self.male = male
        self.age = age

class Letter():
    def __init__(self, char, start, end):
        self.char = char
        self.start = start
        self.end = end

class Word():
    def __init__(self, word, start, end):
        self.word = word
        self.start = start
        self.end = end
        self.letters = []

speakers = []

for speaker in os.listdir('../test-data'):
    try:
        words = pickle.load(open('../test-data/' + speaker + '/audio_arpabet.txt.pkl', 'rb'))
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        male, age = open('../test-data/' + speaker + '/socio.txt').read().split('\n') 
        speakers.append(Speaker(float(latitude), float(longitude), words, age, male))
    except:
        print('Unable to process info for Speaker', speaker)

vowel_length = {
    'AA': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AE': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AH': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AO': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AW': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AX': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AXR': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'AY': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'EH': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'ER': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'EY': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'IH': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'IX': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'IY': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'OW': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'OY': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'UH': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'UW': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []},
    'UX': {'0-20': [], '21-40': [], '41-60': [], '61-80': [], '81-100': []}
}

for speaker in speakers:
    for word in speaker.words:
        for letter in word.letters:
            letter.char = letter.char[1:-1]
            if len(letter.char) == 3:
                letter.char = letter.char[0:2]

            if letter.char in vowel_length:
                age = int(speaker.age)
                if age < 21:
                    vowel_length[letter.char]['0-20'].append(float(letter.end) - float(letter.start))
                elif age < 41:
                    vowel_length[letter.char]['21-40'].append(float(letter.end) - float(letter.start))
                elif age < 61:
                    vowel_length[letter.char]['41-60'].append(float(letter.end) - float(letter.start))
                elif age < 81:
                    vowel_length[letter.char]['61-80'].append(float(letter.end) - float(letter.start))
                elif age < 101:
                    vowel_length[letter.char]['81-100'].append(float(letter.end) - float(letter.start))

for vowel in vowel_length:
    for range_ in vowel_length[vowel]:
        if (len(vowel_length[vowel][range_]) > 0):
            vowel_length[vowel][range_] = sum(vowel_length[vowel][range_]) / len(vowel_length[vowel][range_]) 
        else:
            vowel_length[vowel][range_] = 0

vowel_length_frame = pd.DataFrame(data=vowel_length).T 
print(vowel_length_frame)
vowel_length_frame.plot.bar()
plt.xlabel('Vowel')
plt.ylabel('Average Length in Milliseconds')
plt.title('Average Vowel Length by Speaker Age')
plt.savefig('age_vowel_length.png')
