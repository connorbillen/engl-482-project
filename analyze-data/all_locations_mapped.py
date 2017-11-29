#!/usr/bin/python3

import os
import sys
from MapDrawer import MapDrawer

md = MapDrawer('All Transcription Locations')

for speaker in os.listdir('../test-data/'):
    try:
        latitude, longitude = open('../test-data/' + speaker + '/location.txt').read().split('\n')[1].split(',')
        md.add_points(latitude, longitude)
    except:
        print('No lat/long data for Speaker ', speaker)
        continue

md.draw()
