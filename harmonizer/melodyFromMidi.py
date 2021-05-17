import os
from pretty_midi import PrettyMIDI
import sys

for midipath in sys.argv[1:]:
    full = PrettyMIDI(midipath)
    melody = PrettyMIDI()
    melody.instruments.append(full.instruments[0])
    melody.write(midipath+".melodyOnly.mid")
