#!/usr/bin/python3

import os
import sys
from MapDrawer import MapDrawer

class Speaker:
    def __init__(self, lat, lon, words):
        self.lat = lat
        self.lon = lon
        self.words = words

md = MapDrawer('FER0 vs FA01R vs FRER0')
english_words = open('../test-data/english.txt').read()
speakers = []

for speaker in os.listdir('../test-data/'):
    try:
        transcription = open('../test-data/' + speaker + '/audio_arpabet.txt').read()
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        speakers.append(Speaker(float(latitude), float(longitude), transcription))
    except:
        print('Unable to process info for Speaker', speaker)

# {'FER0', 'FAO1R', 'FRER0'}
FER0_lats = []
FER0_lons = []
FA01R_lats = []
FA01R_lons = []
FRER0_lats = []
FRER0_lons = []

for speaker in speakers:
    if "FER0" in speaker.words:
        FER0_lats.append(speaker.lat)
        FER0_lons.append(speaker.lon)
    elif "FAO1R" in speaker.words:
        FA01R_lats.append(speaker.lat)
        FA01R_lons.append(speaker.lon)
    elif "FRER0" in speaker.words:
        FRER0_lats.append(speaker.lat)
        FRER0_lons.append(speaker.lon)

md.add_points(FER0_lats, FER0_lons)
md.add_points(FA01R_lats, FA01R_lons)
md.add_points(FRER0_lats, FRER0_lons)

md.draw()
