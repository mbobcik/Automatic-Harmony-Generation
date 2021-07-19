#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains script that take proprietary TheoryTab database of parts of songs
and converts them to separate MIDI files.
Each MIDI file contains two tracks. One with melody and one with harmony.

This file is part of my master thesis.
"""
__author__ = "Bc. Martin Bobčík, xbobci00"
__copyright__= "Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"

import os
from sqlite3.dbapi2 import Error
import pandas as pd
import sqlite3
import zlib
import lxml.etree as ET
import utils
#%pip install youtube_dl
import youtube_dl
#%pip install display-xml
import display_xml
#%pip install pychord
from pychord import Chord, Quality
#%pip install xmltodict
#import xmltodict
#%pip install jxmlease
#import jxmlease
#%pip install mido
from utils import *
import sys
from IPython.display import display
from mido import Message, MidiFile, MidiTrack, second2tick, bpm2tempo

def convertDbToMidi(inputDb, outputFolder):

    #initialize connection to the db file
    con = sqlite3.connect(inputDb)

    #Load song parts from DB
    df = pd.read_sql_query("SELECT * FROM parts", con)

    #Load additional informations - mostly for exploring data
    df_parts = pd.read_sql_query(
        "SELECT p.id, p.partid, i.youtubeid, u.url \
        from id2parts p JOIN id2youtube i ON i.id=p.id \
        JOIN url2id u ON u.id=p.id", con)

    #print(df_parts[df_parts.id==32095])
    # Decode XML files from rows
    df['xml'] = df.xml.apply(lambda data: 
        ET.fromstring(zlib.decompress(data).replace(b'%20',b'-')) if data else None)

    # extract some xml metadata
    df['xml_tag'] = df.xml.apply(lambda root: root.tag if root else None).astype('category')
    df['xml_bpm'] = df.xml.apply(lambda root: float(root.find('meta/BPM').text) if root is not None and root.find('meta/BPM') is not None else None).astype('Int64')
    df['xml_key'] = df.xml.apply(lambda root: root.find('meta/key').text if root is not None and root.find('meta/key') is not None else None).astype('category')
    modes = [None, 'ionian (major)','dorian','phyrgian','lydian','mixolydian','aeolian (minor)','locrian']
    df['xml_mode'] = df.xml.apply(lambda root: modes[int(root.find('meta/mode').text)] if root is not None and root.find('meta/mode') is not None else None).astype('category')


    #XML = lambda x: display(display_xml.XML(ET.tostring(x)) if x is not None else None)
    #print(float(df.iloc[0].xml.find('meta/BPM').text))
    #print(ET.tostring( df.iloc[0].xml).decode("UTF-8"))

    #zkouska = df[(df.id == 17213)].iloc[0].xml

    savedCount=0
    errorCount=0

    try:
        os.mkdir(outputFolder)
    except:
        pass

    #For each song part    
    for idx, row in df_parts.iterrows(): 
        ID=row.id

        #boilerplate code
        sonicxml = SonicXMLLayer()
        #lay = sonicxml.addSegmentationLayer(name=f'part {ID} harmony')
        #layseg = sonicxml.addRegionsLayer(name=f'part {ID}',color='#dcf1fa')
        laynotes = sonicxml.addMidiLayer(name=f'part {ID} melody',color='#ff8000')
        laychords = sonicxml.addMidiLayer(name=f'part {ID} harmony',color='#008000')

        # get xml of song part from db
        root = df[(df.id == row.partid) & (df.xml_tag=='theorytab')]
        if not len(root): continue
        root = root.iloc[0].xml

        #get  tempo
        bpmTmp = float(root.find('meta/BPM').text)
        bpm = 120 if bpmTmp <= 0 else bpmTmp  
        meter = int(root.find('meta/beats_in_measure').text)
        tot_measures = sum([int(tts.find('numMeasures').text) for tts in root.findall('data/segment')])
        tot_beats = tot_measures * meter
        bscale = 60.0/bpm

        #key = root.find('meta/key').text
        key_mode = int(root.find('meta/mode').text)

        # init MIDI file and its tracks
        mid = MidiFile(type=1)
        tpb = mid.ticks_per_beat
        #print('tpb',tpb)
        track = MidiTrack()
        mid.tracks.append(track)
        chordsTrack = MidiTrack()
        mid.tracks.append(chordsTrack)
        sonicxml = SonicXMLLayer()

        # init last used time
        segofs = 0
        lasttick = 0
        #for each segment of song part
        for tts in root.findall('data/segment'):
            # for each note in segment
            for ttch in tts.findall('melody/voice/notes/note'):
                #print("NOTE Start-------------------------")

                # get start time of note
                tba = float(ttch.find('start_beat_abs').text)
                #print("start_beat_abs = " + str(tba))

                # get length of the note
                tbd = float(ttch.find('note_length').text)
                #print("note_length = " + str(tbd))
                lstbea = tba + tbd

                # get octave of the note
                tnoteo = int(ttch.find('octave').text)
                #print("octave = " + str(tnoteo))

                # get tonal degree
                tnote = ttch.find('scale_degree').text
                #print("scale_degree = " + str(tnote))

                # check if note is not rest
                if ttch.find('isRest').text.strip() != '1' and tnote != 'rest':
                    midiofs = 0
                    if tnote.endswith('s'): 
                        tnote = tnote[:-1]
                        midiofs = 1
                    elif tnote.endswith('f'): 
                        tnote = tnote[:-1]
                        midiofs = -1
                    tnote = int(tnote)

                    #compute midi note number
                    midinote = getMidiNote(laynotes, key_mode, tnoteo, tnote, midiofs)
                    #print("midinote = " + str(midinote))

                    #Unlike music, tempo in MIDI is not given as 
                    #beats per minute, but rather in microseconds per beat.

                    #The default tempo is 500000 microseconds per beat, 
                    # which is 120 beats per minute. 
                    # The meta message ‘set_tempo’ can be used to change tempo during a song.
                    
                    #compute start time of note in midi
                    t0 = second2tick((segofs+tba)*bscale,
                                        ticks_per_beat=mid.ticks_per_beat,
                                        tempo=bpm2tempo(bpm))

                    t = int(t0) - lasttick 

                    #print((segofs+tba)*bscale, lasttick, t)
                    #if(t<0):
                    #    print(t)

                    track.append(Message('note_on', note=midinote, velocity=127, time=t))
                    
                    #compute end time of note in midi
                    t1 = second2tick((segofs+tba+tbd)*bscale,
                                        ticks_per_beat=mid.ticks_per_beat,
                                        tempo=bpm2tempo(bpm))
                    t = int(t1) - int(t0) 
                    #if(t<0):
                    #    print(t)
                    #print(t)
                    track.append(Message('note_off', note=midinote, velocity=127, time=t))
                    
                    # save last used time
                    lasttick = int(t1)

            #reset last used time
            segofs = 0
            lasttick = 0
            #for each chord in segment
            for ttch in tts.findall('harmony/chord'):
                #print("CHORD Start-------------------------")

                #get start time
                tba = float(ttch.find('start_beat_abs').text)
                #print("start_beat_abs = " + str(tba))

                #get chord duration_length
                tbd = float(ttch.find('chord_duration').text)
                #print("chord_duration = " + str(tbd))

                # fix chord octave
                tnoteo = 0
                #print("octave = " + str(tnoteo))

                # get tonal degree of chords base tone
                tnote = ttch.find('sd').text
                #print("scale_degree = " + str(tnote))

                # check for rest
                if ttch.find('isRest').text.strip() != '1' and tnote != 'rest':
                    midiofs = 0
                    if tnote.endswith('s'): 
                        tnote = tnote[:-1]
                        midiofs = 1
                    elif tnote.endswith('f'): 
                        tnote = tnote[:-1]
                        midiofs = -1
                    tnote = int(tnote)

                    # compute tones in chord
                    midiChord = getMidiChord(laynotes,key_mode,-1,tnote,midiofs)

                    #compute starting time of chord
                    t0 = second2tick((segofs+tba)*bscale,
                                        ticks_per_beat=mid.ticks_per_beat,
                                        tempo=bpm2tempo(bpm))
                    t = int(t0) - lasttick 
                    
                    # tones are starting simultaneously > delta time is zero
                                                                                         # time since last event 
                    chordsTrack.append(Message('note_on', note=midiChord[0], velocity=127, time=t, channel=0))
                    chordsTrack.append(Message('note_on', note=midiChord[1], velocity=127, time=0, channel=0))
                    chordsTrack.append(Message('note_on', note=midiChord[2], velocity=127, time=0, channel=0))
                    
                    #compute end time
                    t1 = second2tick((segofs+tba+tbd)*bscale,
                                        ticks_per_beat=mid.ticks_per_beat,
                                        tempo=bpm2tempo(bpm))                                                                     # 0 = starting simultaneously
                    t = int(t1) - int(t0) 
                    chordsTrack.append(Message('note_off', note=midiChord[0], velocity=127, time=t, channel=0))
                    chordsTrack.append(Message('note_off', note=midiChord[1], velocity=127, time=0, channel=0))
                    chordsTrack.append(Message('note_off', note=midiChord[2], velocity=127, time=0, channel=0))

                    #update last used time
                    lasttick = int(t1)

            # update time offset based on segments
            measures = int(tts.find('numMeasures').text)
            segofs += measures * meter

        try:
            
            newFilePath=f'{outputFolder}/{ID}__part{row.partid}.mid'

            #check if song has both melody and harmony
            assert len(mid.tracks) == 2 and len(mid.tracks[0]) != 0 and len(mid.tracks[1]) != 0, "song dont have melody or harmony"
            
            mid.save(newFilePath)
            try:
                #reopen the file and check for both tracks again
                test=MidiFile(newFilePath)
                assert len(test.tracks) == 2

                savedCount+=1
                
            except:
                os.remove(newFilePath)
                raise Error(f"File {newFilePath} could not be opened after creation - was deleted")
        except Exception as e:  
            if os.path.isfile(newFilePath):
                os.remove(newFilePath)
            errorCount+=1
            print(f"ERROR: {ID}__part{row.partid}.mid failed to save. - saved={savedCount} errors={errorCount} - {e}")
    
    print(f"Total saved: {savedCount} Total Errors: {errorCount}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("bad arguments.")
        print("usage:")
        print("py dbToMIDI.py inputDbFile.db outputFolder")
        exit()

    convertDbToMidi(sys.argv[1],sys.argv[2])