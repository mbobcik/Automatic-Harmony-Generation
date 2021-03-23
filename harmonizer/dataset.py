import numpy as np
import torch
import pandas as pd
from collections import Counter
from mido import MidiFile,MidiTrack, tick2second,MetaMessage
import pretty_midi
from pretty_midi import PrettyMIDI
import os
from stopwatch import Stopwatch
from prettierMidi import PrettierMidi

class Dataset( torch.utils.data.Dataset):
    def __init__(self, folder, divideSecondBy):
        self.folder=folder
        self.divideSecondBy= divideSecondBy
        self.toOnesAndZeroes = lambda x: x/127
        self.tmpPath = "tmp.mid"

    def loadMidiFileAsChroma(self, path):
        wholeMidi= MidiFile(path)
        tmpMido = MidiFile()
        tmpMido.tracks.append(wholeMidi.tracks[0])
        tmpMido.save(self.tmpPath)
        melodyPretty=PrettyMIDI(self.tmpPath)
        melodyChroma=melodyPretty.get_chroma(fs=self.divideSecondBy)

        tmpMido.tracks[0]=wholeMidi.tracks[1]
        tmpMido.save(self.tmpPath)
        harmonyPretty=PrettyMIDI(self.tmpPath)
        harmonyChroma=harmonyPretty.get_chroma(fs=self.divideSecondBy)

        #os.remove(tmpPath)
        return (self.toOnesAndZeroes(melodyChroma), self.toOnesAndZeroes(harmonyChroma))
    
    def loadWholeFolder(self):
        resultMelodies=list()
        resultHarmonies= list()
        counter=0
        sw=Stopwatch()
        sw.start()
        for file in os.scandir(self.folder):
            melody, harmony = self.loadMidiFileAsChroma(file)
            resultMelodies.append(melody)
            resultHarmonies.append(harmony)
            counter=counter+1
            if counter%500==0:
                print(f"File number {counter} is saved in {sw.elapsed} seconds! {file} -  ({(sw.elapsed/counter)*1000}ms file time)")
        sw.stop()
        print(f"Done -  {counter} files in {sw.elapsed}s ({(sw.elapsed/counter)*1000}ms file time)")
        return (resultMelodies, resultHarmonies)

if __name__ == "__main__":  
    ds=Dataset("midi", 4)
    #print(ds.loadMidiFileAsChroma("midi/4346__part554176.mid")[1])
    ds.loadWholeFolder()
