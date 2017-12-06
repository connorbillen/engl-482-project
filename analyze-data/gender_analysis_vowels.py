#!/usr/bin/python3

import os
import sys
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class Speaker:
    def __init__(self, lat, lon, words, male, age):
        self.lat = lat
        self.lon = lon
        self.words = words
        self.male = male
        self.age = age

for speaker in os.lisdir('../test-data'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read()
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        speakers.append(Speaker(float(latitude), float(longitude), transcription))
    except:
        print('Unable to process info for Speaker', speaker)
