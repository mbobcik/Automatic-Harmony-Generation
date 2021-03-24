import numpy as np
import torch
import pandas as pd
from collections import Counter
from mido import MidiFile,MidiTrack, tick2second,MetaMessage
import pretty_midi
from pretty_midi import PrettyMIDI
import os
from stopwatch import Stopwatch

class Dataset( torch.utils.data.Dataset):
    def __init__(self, folder, divideSecondBy):
        self.folder=folder
        self.divideSecondBy= divideSecondBy
        self.toOnesAndZeroes = lambda x: x/127
        self.tmpPath = "tmp.mid"

    def loadMidiFileAsChroma(self, path):
        wholeMidi= PrettyMIDI(path)
        assert len(wholeMidi.instruments) == 2, f"File {path} dont have two tracks"
        melodyChroma=wholeMidi.instruments[0].get_chroma(fs=self.divideSecondBy)
        harmonyChroma=wholeMidi.instruments[1].get_chroma(fs=self.divideSecondBy)

        #os.remove(tmpPath)
        return (self.toOnesAndZeroes(melodyChroma), self.toOnesAndZeroes(harmonyChroma))
    
    def loadWholeFolder(self):
        resultMelodies=list()
        resultHarmonies= list()
        counter=0
        sw=Stopwatch()
        sw.start()
        for file in os.scandir(self.folder):

            try:
                melody, harmony = self.loadMidiFileAsChroma(file.path)
                resultMelodies.append(melody)
                resultHarmonies.append(harmony)
            except Exception as e:
                # asi vsechny prvky pole, pokud 0, pak error, jinak asi pohoda
                
                print(f"ERROR: {e}")
                continue
            counter=counter+1
            if counter%500==0:
                print(f"File number {counter} is saved in {sw.elapsed} seconds! {file} -  ({(sw.elapsed/counter)*1000}ms file time)")
        sw.stop()
        print(f"Done -  {counter} files in {sw.elapsed}s ({(sw.elapsed/counter)*1000}ms file time)")
        return (resultMelodies, resultHarmonies)

if __name__ == "__main__":  
    ds=Dataset("midi", 4)
    #print(ds.loadMidiFileAsChroma("midi/4346__part554176.mid")[1])
    melodies, harmonies = ds.loadWholeFolder()
    melodyMaxLen=0
    harmonyMaxLen=0
    sw=Stopwatch()
    sw.start()
    counter = 0
    for melody in  melodies:
      melodyMaxLen = melodyMaxLen if melodyMaxLen > melody.shape[1] else melody.shape[1]
      counter+=1
    melodiesTime=sw.elapsed
    for harmony in  harmonies:
          harmonyMaxLen = harmonyMaxLen if harmonyMaxLen > harmony.shape[1] else harmony.shape[1]
    sw.stop()
    print("melody max len = {} in {}s({}) harmony max len = {} in {}s".format(melodyMaxLen,melodiesTime,counter, harmonyMaxLen, sw.elapsed))