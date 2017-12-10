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
    'AA': {'male': [], 'female': []},
    'AE': {'male': [], 'female': []},
    'AH': {'male': [], 'female': []},
    'AO': {'male': [], 'female': []},
    'AW': {'male': [], 'female': []},
    'AX': {'male': [], 'female': []},
    'AXR': {'male': [], 'female': []},
    'AY': {'male': [], 'female': []},
    'EH': {'male': [], 'female': []},
    'ER': {'male': [], 'female': []},
    'EY': {'male': [], 'female': []},
    'IH': {'male': [], 'female': []},
    'IX': {'male': [], 'female': []},
    'IY': {'male': [], 'female': []},
    'OW': {'male': [], 'female': []},
    'OY': {'male': [], 'female': []},
    'UH': {'male': [], 'female': []},
    'UW': {'male': [], 'female': []},
    'UX': {'male': [], 'female': []}
}

for speaker in speakers:
    for word in speaker.words:
        for letter in word.letters:
            letter.char = letter.char[1:-1]
            if len(letter.char) == 3:
                letter.char = letter.char[0:2]

            if letter.char in vowel_length:
                if speaker.male == "True":
                    vowel_length[letter.char]['male'].append(float(letter.end) - float(letter.start))
                else:
                    vowel_length[letter.char]['female'].append(float(letter.end) - float(letter.start))

for vowel in vowel_length:
    if len(vowel_length[vowel]['male']) > 0:
        vowel_length[vowel]['male'] = sum(vowel_length[vowel]['male']) / len(vowel_length[vowel]['male'])
    else:
        vowel_length[vowel]['male'] = 0

    if len(vowel_length[vowel]['female']) > 0:
        vowel_length[vowel]['female'] = sum(vowel_length[vowel]['female']) / len(vowel_length[vowel]['female'])
    else:
        vowel_length[vowel]['female'] = 0

vowel_length_frame = pd.DataFrame(data=vowel_length).T 
print(vowel_length_frame)
vowel_length_frame.plot.bar()
plt.xlabel('Vowel')
plt.ylabel('Average Length in Milliseconds')
plt.title('Average Vowel Length by Speaker Gender')
plt.savefig('gender_vowel_length.png')
