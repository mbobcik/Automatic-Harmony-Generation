#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains script that extracts track with melody and saves it to separate midi file.
It is assumed that the melody is in first track.
Paths to MIDI files to convert should be specified as arguments of script.
New midi files, with .melodyOnly.mid suffix, will be created next to the specified files.

This file is part of my master thesis.
"""
__author__ = "Bc. Martin Bobčík, xbobci00"
__copyright__= "Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"


import os
from pretty_midi import PrettyMIDI
import sys

if len(sys.argv[1:]) == 0 :
    print(__doc__)

for midipath in sys.argv[1:]:
    #load midi file
    full = PrettyMIDI(midipath)
    melody = PrettyMIDI()
    #save track with melody to another file
    melody.instruments.append(full.instruments[0])
    melody.write(midipath+".melodyOnly.mid")
