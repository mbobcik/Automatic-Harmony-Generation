#!/bin/bash
# Script which will automatically prepare dataset for training neural network.
# Prerequisite is to run scripts prerequisities.sh and install.sh
# First argument is folder with MIDI files.
# Second argument is the SQLite DB file with songs.
# If left unspecified, the conversion from DB file is omited.
# This file is part of my Master thesis.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology

if [ -z "$1" ] 
    then
    echo "Bundle file with model not specified!"
    echo "Script which will automatically prepare dataset for training neural network.
Prerequisite is to run scripts prerequisities.sh and install.sh
First argument is folder with MIDI files.
Second argument is the SQLite DB file with songs.
If left unspecified, the conversion from DB file is omited.
This file is part of my Master thesis.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    
    exit 1
fi

if [ -z "$2" ] 
    then
    echo "MIDI file with melody not specified!"
        echo "Script which will automatically prepare dataset for training neural network.
Prerequisite is to run scripts prerequisities.sh and install.sh
First argument is folder with MIDI files.
Second argument is the SQLite DB file with songs.
If left unspecified, the conversion from DB file is omited.
This file is part of my Master thesis.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

if [ -z "$3" ] 
    then
    echo "Number of measures not specified!"
        echo "Script which will automatically prepare dataset for training neural network.
Prerequisite is to run scripts prerequisities.sh and install.sh
First argument is folder with MIDI files.
Second argument is the SQLite DB file with songs.
If left unspecified, the conversion from DB file is omited.
This file is part of my Master thesis.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

BUNDLEFILE=$(readlink -f $1)
MIDI=$(readlink -f $2)
STEPS=$( expr $3 \* 32 )
echo $STEPS
polyphony_rnn_generate \
    --bundle_file="$BUNDLEFILE" \
    --output_dir=./generated \
    --num_outputs=10 \
    --num_steps=$STEPS \
    --primer_midi="$MIDI" \
    --condition_on_primer=false \
    --inject_primer_during_generation=true    