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

speakers = []

for speaker in os.listdir('../test-data'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read()
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        age, male = open('../test-data/' + speaker + '/socio.txt').read().split('\n') 
        speakers.append(Speaker(float(latitude), float(longitude), transcription, male, age))
    except:
        print('Unable to process info for Speaker', speaker)

ages = []
for speaker in speakers:
    ages.append(int(speaker.age))

plt.hist(ages, bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],align='mid', rwidth=.75)
plt.xlabel('Age Range')
plt.ylabel('Frequency')
plt.title('Age Distribution')
plt.savefig('age_distro.png')
plt.show()
