#!/usr/bin/python3

import os
import sys
import pickle
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class Speaker:
    def __init__(self, lat, lon, words, male, age, state):
        self.lat = lat
        self.lon = lon
        self.words = words
        self.male = male
        self.age = age
        self.state = state

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
        state = open('../test-data/' + speaker + '/location.txt').read().split('\n')[0].split(',')[-2:-1][0].strip()
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        male, age = open('../test-data/' + speaker + '/socio.txt').read().split('\n') 
        speakers.append(Speaker(float(latitude), float(longitude), words, age, male, state))
    except:
        print('Unable to process info for Speaker', speaker)

regions = {
    'Northeast': ['maine', 'new hampshire', 'vermont', 'massachusetts', 'rhode island', 'connecticut', 'new york', 'pennsylvania', 'new jersey'],
    'Midwest': ['wisconsin', 'michigan', 'illinois', 'indiana', 'ohio', 'north dakota', 'south dakota', 'nebraska', 'kansas', 'minnesota', 'iowa'],
    'South': ['delaware', 'maryland', 'district of columbia', 'virginia', 'west virginia', 'north carolina', 'south carolina', 'georgia', 'florida', 'kentucky', 'tennesee', 'mississippi', 'alabama', 'oklahoma', 'texas', 'arkansas', 'louisiana'],
    'West': ['idaho', 'montana', 'wyoming', 'nevada', 'utah', 'colorado', 'arizona', 'new mexico', 'alaska', 'washington', 'oregon', 'california', 'hawaii']
}

vowel_length = {
    'AA': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AE': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AH': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AO': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AW': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AX': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AXR': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'AY': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'EH': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'ER': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'EY': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'IH': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'IX': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'IY': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'OW': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'OY': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'UH': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'UW': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []},
    'UX': {'Northeast': [], 'Midwest': [], 'South': [], 'West': []}
}

for speaker in speakers:
    for word in speaker.words:
        for letter in word.letters:
            letter.char = letter.char[1:-1]
            if len(letter.char) == 3:
                letter.char = letter.char[0:2]

            if letter.char in vowel_length:
                if speaker.state in regions['Northeast']:
                    vowel_length[letter.char]['Northeast'].append(letter.end - letter.start)
                elif speaker.state in regions['Midwest']:
                    vowel_length[letter.char]['Midwest'].append(letter.end - letter.start)
                elif speaker.state in regions['South']:
                    vowel_length[letter.char]['South'].append(letter.end - letter.start)
                elif speaker.state in regions['West']:
                    vowel_length[letter.char]['West'].append(letter.end - letter.start)


for vowel in vowel_length:
    for range_ in vowel_length[vowel]:
        if (len(vowel_length[vowel][range_]) > 0):
            vowel_length[vowel][range_] = sum(vowel_length[vowel][range_]) / len(vowel_length[vowel][range_]) 
        else:
            vowel_length[vowel][range_] = 0

vowel_length_frame = pd.DataFrame(data=vowel_length).T 
print(vowel_length_frame)
vowel_length_frame.plot.bar()
plt.show()
