#!/usr/bin/python3

import os
import sys
from MapDrawer import MapDrawer

class Speaker:
    def __init__(self, lat, lon, words):
        self.lat = lat
        self.lon = lon
        self.words = words

# 'TIH0', 'TUW1', 'TAH0'
md = MapDrawer('TIH0 vs TUW1 vs TAH0')
english_words = open('../test-data/english.txt').read()
speakers = []

for speaker in os.listdir('../test-data/'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read()
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        speakers.append(Speaker(float(latitude), float(longitude), transcription))
    except:
        print('Unable to process info for Speaker', speaker)

TIH0_lats = []
TIH0_lons = []
TUW1_lats = []
TUW1_lons = []
TAH0_lats = []
TAH0_lons = []

for speaker in speakers:
    if "TIH0" in speaker.words:
        TIH0_lats.append(speaker.lat)
        TIH0_lons.append(speaker.lon)
    if "TUW1" in speaker.words:
        TUW1_lats.append(speaker.lat)
        TUW1_lons.append(speaker.lon)
    if "TAH0" in speaker.words:
        TAH0_lats.append(speaker.lat)
        TAH0_lons.append(speaker.lon)

print(len(TIH0_lats))
print(len(TUW1_lats))
print(len(TAH0_lats))

md.add_points(TIH0_lats, TIH0_lons)
md.add_points(TUW1_lats, TUW1_lons)
md.add_points(TAH0_lats, TAH0_lons)

md.draw()
