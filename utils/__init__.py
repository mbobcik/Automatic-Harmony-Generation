from collections import deque
import lxml.etree as ET

MODES = {1:'ionian', #major
         2:'dorian', 3:'phyrgian', 4:'lydian', 5:'mixolydian', 
         6:'aeolian', #minor
         7:'locrian'}

def getNotesOfKey(key,mode):
    if isinstance(mode, int):
        #modes: ionian,dorian,phyrgian, lydian, mixolydian,aeolian,locrian
        assert 1 <= mode <= 7
    else:
        mode = {'maj':1, 'min':6, 'ionian':1,'dorian':2,'phyrgian':3,'lydian':4,'mixolydian':5,'aeolian':6,'locrian':7}[mode]
        #mode = {1:'maj',6:'min'}[mode]
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    NOTES_ALT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    if key in NOTES:
        ofs = NOTES.index(key)
    else:
        ofs = NOTES_ALT.index(key)
    steps = deque([2,2,1,2,2,2,1])
    steps.rotate(-mode+1)
    #steps = {'maj':[2,2,1,2,2,2,1],'min':[2,1,2,2,1,2,2]}
    #print(steps)
    ls = len(steps)#[mode])
    ln = len(NOTES)
    nnote,noctave = [],[]
    for i in range(8):
        #print(NOTES[ofs % ln], ofs // ln)
        nnote.append(NOTES[ofs % ln])
        noctave.append(ofs // ln)
        ofs +=  steps[i % ls]

    return nnote, noctave


class XMLLayer:
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    NOTES_ALT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    OCTAVES = list(range(11))
    NOTES_IN_OCTAVE = len(NOTES)

    def __init__(self, top, l, m,d):
        self.l = l
        self.m = m
        self.d = d
        self.top = top

    def addInstant(self, time_seconds, label=None):
        d = {'frame':str(self.top.time2frame(time_seconds))}
        if label: d['label'] = label
        return ET.SubElement(self.d, 'point', d)
        
    def addMidiNote(self, time_seconds, duration_seconds, value, label=None, volume=1.0):
        d = {'frame':str(self.top.time2frame(time_seconds)), 'value':str(value), 'duration':str(self.top.time2frame(duration_seconds)), 'level':'%.1f' % volume}
        if label: d['label'] = label
        return ET.SubElement(self.d, 'point', d)

    def noteToMidiNumber(self, note, octave=4):
        assert note in XMLLayer.NOTES or note in XMLLayer.NOTES_ALT, 'Invalid note'
        assert octave in XMLLayer.OCTAVES, 'Invalid octave'

        note = XMLLayer.NOTES.index(note) if note in XMLLayer.NOTES else XMLLayer.NOTES_ALT.index(note)
        note += (XMLLayer.NOTES_IN_OCTAVE * octave)

        assert 0 <= note <= 127, 'Out of range'

        return note

class SonicXMLLayer:
    def __init__(self, sampleRate=44100):
        self.top = ET.Element('sv')
        #self.top = ET.fromstring("""<sv><data /><display /></sv>""")
        self.data = ET.SubElement(self.top,'data')
        self.display = ET.SubElement(self.top,'display')
        self.layers = 0
        self.models = 5
        self.datasets = 5
        self.color = 0
        self.sr = sampleRate

    def td(self, tpl, dct):
        d = dict(tpl)
        for lk in d:
            if d[lk] != None:
                d[lk] = str(d[lk])
        for lk in dct:
            if dct[lk] != None:
                d[lk] = str(dct[lk])
        return d

    def time2frame(self, time_seconds):#cas v sekundach
        return int(self.sr*time_seconds)


    def addLayer(self, type='timeinstants', style=0, dimensions=1, color=None, name='',resolution=1, layparams={}, modelparams={},datasetparams={}):
        if color == None:
            color = ['#d01c8b','#4dac26','#7b3294','#ca0020','#2b83ba','#404040','#e66101'][self.color % 7]
            self.color += 1
        self.layers += 1
        self.models += 1
        self.datasets += 1
        l = ET.SubElement(self.display,'layer',self.td(layparams, {'id':self.layers,'type':type,'name':name,'model':self.models,'plotStyle':style,'colour':color, 'darkBackground':'false'}))
#        <layer id="1" type="timeinstants" name="Time Instants &lt;2&gt;" model="6"  plotStyle="1" colourName="Black" colour="#000000" darkBackground="false" />
        m = ET.SubElement(self.data,'model',self.td(modelparams, {'id':self.models,'name':name,'sampleRate':self.sr, 'type':'sparse', 'dimensions':dimensions, 'resolution':resolution,'notifyOnAdd':'true', 'dataset':self.datasets}))
        d = ET.SubElement(self.data,'dataset',self.td(datasetparams, {'id':self.datasets, 'dimensions':dimensions}))
#       <model id="6" name="--cXBgR-A-I-parts.txt" sampleRate="44100" type="sparse" dimensions="1" resolution="1" notifyOnAdd="true" dataset="5" />
        return XMLLayer(self, l,m,d)

    def addMidiLayer(self, name='',color=None):
        return self.addLayer(name=name, color=color, type='notes', style=None, dimensions=3, resolution=2048, layparams={'verticalScale':3, 'scaleMinimum':0, 'scaleMaximum':0}, modelparams={'subtype':'note', 'valueQuantization':0, 'minimum':0,'maximum':127,'units':'MIDI units'})

    def addSegmentationLayer(self, name='',color=None):
        return self.addLayer(type='timeinstants', style=1, name=name, color=color)

    def addInstantLayer(self, name='',color=None):
        return self.addLayer(type='timeinstants', name=name, color=color)

    def addRegionsLayer(self, name='',color=None):
        return self.addLayer(type='regions', style=1, dimensions=3, name=name, color=color, layparams={'verticalScale':0}, modelparams={'subtype':"region",'valueQuantization':0, 'minimum':0,'maximum':1,'units':''})

    def __bytes__(self):
        #s = '<?xml version="1.0" encoding="UTF-8" ?><!DOCTYPE sonic-visualiser>'.encode('utf8')
        #s += prettify(self.top) #ET.ElementTree(self.top).write(f, 'utf-8')
        return ET.tostring(self.top, encoding="UTF-8",
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE sonic-visualiser>')

    def write(self, fp):
        fp.write(bytes(self))