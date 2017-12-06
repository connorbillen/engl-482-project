#!/usr/bin/python3

import os
import sys
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class Speaker:
    def __init__(self, lat, lon, words, male=True, age=63):
        self.lat = lat
        self.lon = lon
        self.words = words
        self.male = male
        self.age = age

speakers = []

for speaker in os.listdir('../test-data'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read()
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        age, male = open('../test-data/' + speaker + '/socio.txt').read().split('\n') 
        speakers.append(Speaker(float(latitude), float(longitude), transcription))
    except:
        print('Unable to process info for Speaker', speaker)

for speaker in speakers:
    # logic
