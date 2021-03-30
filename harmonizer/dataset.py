import numpy as np
import torch
import pandas as pd
from collections import Counter
from pretty_midi import PrettyMIDI
import os
from stopwatch import Stopwatch
from progress import progress

class Dataset( torch.utils.data.Dataset):
    def __init__(self, sequence_length=4, folder="midi", divideSecondBy=4):
        self.sequence_length=sequence_length
        self.folder=folder
        self.divideSecondBy= divideSecondBy
        self.toOnesAndZeroes = lambda x: x/127
        numpyFilez="numpyData.npz"
        if os.path.exists(numpyFilez):
            sw=Stopwatch()
            sw.start()


            npzFile= np.load(numpyFilez)
            self.melodiesArr=npzFile['melodies']
            self.harmoniesArr=npzFile['harmonies']
            assert self.melodiesArr.shape == self.harmoniesArr.shape, "Melodies and harmonies arrays should be the same shape"
            del npzFile

            sw.stop()
            print(f"Done in {sw.elapsed}s")

        else:
            self.melodiesArr, self.harmoniesArr = self.loadWholeFolder()
            assert self.melodiesArr.shape == self.harmoniesArr.shape, "Melodies and harmonies arrays should be the same shape"
            np.savez(numpyFilez, melodies=self.melodiesArr, harmonies=self.harmoniesArr)

    def loadMidiFileAsChroma(self, path):
        wholeMidi= PrettyMIDI(path)
        assert len(wholeMidi.instruments) == 2, f"File {path} dont have two tracks"
        melodyChroma=wholeMidi.instruments[0].get_chroma(fs=self.divideSecondBy)
        harmonyChroma=wholeMidi.instruments[1].get_chroma(fs=self.divideSecondBy)

        #make melody and harmony same length (fill with zeroes/no tones)
        if melodyChroma.shape[1] > harmonyChroma.shape[1]:
            addShape=(12,melodyChroma.shape[1] - harmonyChroma.shape[1])
            harmonyChroma = np.append(harmonyChroma,np.zeros(shape=addShape), axis=1)
        elif harmonyChroma.shape[1] > melodyChroma.shape[1]:
            addShape=(12,harmonyChroma.shape[1] - melodyChroma.shape[1])
            melodyChroma =np.append(melodyChroma,np.zeros(shape=addShape), axis=1)

        return (self.toOnesAndZeroes(melodyChroma), self.toOnesAndZeroes(harmonyChroma))
    
    def loadWholeFolder(self):
        resultMelodies=np.zeros((12,1))
        resultHarmonies= np.zeros((12,1))
        counter=0
        total=len([name for name in os.scandir(self.folder)])
        sw=Stopwatch()
        sw.start()
        for file in os.scandir(self.folder):
            try:
                melody, harmony = self.loadMidiFileAsChroma(file.path)
                resultMelodies = np.append(resultMelodies, melody, axis=1)
                resultHarmonies = np.append(resultHarmonies, harmony, axis=1)
            except Exception as e:
                print(f"ERROR with file {file.path}: {e}")
                continue
            counter=counter+1
            if counter%10==0:
                progress(counter,total,
                    "Loading midi files - Estimated time {:.0f}s ".format((sw.elapsed/counter)*(total-counter)))
        sw.stop()
        print()
        print(f"Done -  {counter} files in {sw.elapsed}s ({(sw.elapsed/counter)*1000}ms file time)")
        return (resultMelodies.T[1:], resultHarmonies.T[1:])

    def flattenListToArray(self, list, message=""):
        resArray=np.zeros((12,1))
        total = len(list)
        counter = 0
        for arr in list:
            resArray = np.append(resArray, arr, axis=1)
            counter += 1
            progress(counter, total, message)
        print()
        return resArray

    def __len__(self):
        return self.melodiesArr.shape[0] - self.sequence_length

    def __getitem__(self, index):
        return (
            torch.tensor(self.melodiesArr[index: index+self.sequence_length]),
            torch.tensor(self.harmoniesArr[index: index+self.sequence_length])
        )

if __name__ == "__main__": 

    ds=Dataset(4,"midi", 4)
    #print(ds.loadMidiFileAsChroma("midi/4346__part554176.mid")[1])
    #melodies, harmonies = ds.loadWholeFolder()
    #melodyMaxLen=0
    #harmonyMaxLen=0
    #sw=Stopwatch()
    #sw.start()
    #counter = 0
    #for melody in  melodies:
    #  melodyMaxLen = melodyMaxLen if melodyMaxLen > melody.shape[1] else melody.shape[1]
    #  counter+=1
    #melodiesTime=sw.elapsed
    #for harmony in  harmonies:
    #      harmonyMaxLen = harmonyMaxLen if harmonyMaxLen > harmony.shape[1] else harmony.shape[1]
    #sw.stop()
    #print("melody max len = {} in {}s({}) harmony max len = {} in {}s".format(melodyMaxLen,melodiesTime,counter, harmonyMaxLen, sw.elapsed))
    #print(f"dataset len = {len(ds)}")
    a=ds[0]
    print(a)
    pass