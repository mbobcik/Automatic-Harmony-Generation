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
from IPython.display import display
from mido import Message, MidiFile, MidiTrack, second2tick, bpm2tempo


con = sqlite3.connect("data-all.db")

#Nacteni dat z DB 
df = pd.read_sql_query("SELECT * FROM parts", con)

df_parts = pd.read_sql_query(
    "SELECT p.id, p.partid, i.youtubeid, u.url \
    from id2parts p JOIN id2youtube i ON i.id=p.id \
    JOIN url2id u ON u.id=p.id", con)

#print(df_parts[df_parts.id==32095])
# Dekodovani XML
df['xml'] = df.xml.apply(lambda data: 
    ET.fromstring(zlib.decompress(data).replace(b'%20',b'-')) if data else None)

# Extrakce metadat z XML

df['xml_tag'] = df.xml.apply(lambda root: root.tag if root else None).astype('category')
df['xml_bpm'] = df.xml.apply(lambda root: float(root.find('meta/BPM').text) if root is not None and root.find('meta/BPM') is not None else None).astype('Int64')
df['xml_key'] = df.xml.apply(lambda root: root.find('meta/key').text if root is not None and root.find('meta/key') is not None else None).astype('category')
modes = [None, 'ionian (major)','dorian','phyrgian','lydian','mixolydian','aeolian (minor)','locrian']
df['xml_mode'] = df.xml.apply(lambda root: modes[int(root.find('meta/mode').text)] if root is not None and root.find('meta/mode') is not None else None).astype('category')


#XML = lambda x: display(display_xml.XML(ET.tostring(x)) if x is not None else None)
#print(float(df.iloc[0].xml.find('meta/BPM').text))
#print(ET.tostring( df.iloc[0].xml).decode("UTF-8"))



for idx, row in df_parts.iterrows():
    sonicxml = SonicXMLLayer()
    ID=row.id

    lay = sonicxml.addSegmentationLayer(name=f'part {ID} harmony')
    layseg = sonicxml.addRegionsLayer(name=f'part {ID}',color='#dcf1fa')
    laynotes = sonicxml.addMidiLayer(name=f'part {ID} melody',color='#ff8000')
    laychords = sonicxml.addMidiLayer(name=f'part {ID} harmony',color='#008000')

    root = df[(df.id == row.partid) & (df.xml_tag=='theorytab')]
    if not len(root): continue
    root = root.iloc[0].xml
    bpm = float(root.find('meta/BPM').text)
    meter = int(root.find('meta/beats_in_measure').text)
    key = root.find('meta/key').text
    key_mode = int(root.find('meta/mode').text)

    tot_measures = sum([int(tts.find('numMeasures').text) for tts in root.findall('data/segment')])
    tot_beats = tot_measures * meter
    bscale = 60.0/bpm

    mid = MidiFile(type=0)
    tpb = mid.ticks_per_beat
    print('tpb',tpb)
    track = MidiTrack()
    mid.tracks.append(track)

    sonicxml = SonicXMLLayer()

    segofs = 0
    lasttick = 0
    for tts in root.findall('data/segment'):
        for ttch in tts.findall('melody/voice/notes/note'):
            tba = float(ttch.find('start_beat_abs').text)
            tbd = float(ttch.find('note_length').text)
            lstbea = tba + tbd
            tnotel= float(ttch.find('note_length').text)
            tnoteo = int(ttch.find('octave').text)
            tnote = ttch.find('scale_degree').text
            if ttch.find('isRest').text.strip() != '1' and tnote != 'rest':
                midiofs = 0
                if tnote.endswith('s'): 
                    tnote = tnote[:-1]
                    midiofs = 1
                elif tnote.endswith('f'): 
                    tnote = tnote[:-1]
                    midiofs = -1
                tnote = int(tnote)
                midinote, midinoteo = getNotesOfKey(key, key_mode)
                midinote, midinoteo = midinote[tnote-1], midinoteo[tnote-1]
                midinote = laynotes.noteToMidiNumber(midinote, tnoteo + midinoteo+ 4) + midiofs
                
                #Unlike music, tempo in MIDI is not given as 
                #beats per minute, but rather in microseconds per beat.

                #The default tempo is 500000 microseconds per beat, 
                # which is 120 beats per minute. 
                # The meta message ‘set_tempo’ can be used to change tempo during a song.
                t0 = second2tick((segofs+tba)*bscale,
                                    ticks_per_beat=mid.ticks_per_beat,
                                    tempo=bpm2tempo(bpm))
                t1 = second2tick((segofs+tba+tbd)*bscale,
                                    ticks_per_beat=mid.ticks_per_beat,
                                    tempo=bpm2tempo(bpm))
                t = int(t0) - lasttick 
                #print((segofs+tba)*bscale, lasttick, t)
                track.append(Message('note_on', note=midinote, velocity=127, time=t))
                t = int(t1) - int(t0) 
                #print(t)
                track.append(Message('note_off', note=midinote, velocity=127, time=t))
                lasttick = int(t1)

        measures = int(tts.find('numMeasures').text)
        segofs += measures * meter

        print(ET.tostring(tts).decode("UTF-8"))
            
    
    mid.save(f'{ID}__part{row.partid}.mid')