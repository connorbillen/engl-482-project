#!/usr/bin/python3

import os
import sys
import pickle
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
        age, male = open('../test-data/' + speaker + '/socio.txt').read().split('\n') 
        speakers.append(Speaker(float(latitude), float(longitude), words, age, male))
    except:
        print('Unable to process info for Speaker', speaker)

for speaker in speakers:
    print(speaker.words)
