#!/bin/bash
# Script which will automatically prepare dataset for training neural network.
# Prerequisite is to run scripts prerequisities.sh and install.sh
# First argument is folder with MIDI files.
# Second argument is the SQLite DB file with songs.
# If first argument is -s and second path to the noteSequence file, 
# then script will make only SequenceExamples from that file.
# If left unspecified, the conversion from DB file is omited.
# This file is part of my Master thesis.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology

#check argument for folder with midi files
if [ -z "$1" ] 
    then
    echo "Folder with MIDI files not specified!"
    echo "Script which will automatically prepare dataset for training neural network.
Prerequisite is to run scripts prerequisities.sh and install.sh
First argument is folder with MIDI files.
Second argument is the SQLite DB file with songs.

If first argument is -s and second path to the noteSequence file, 
then script will make only SequenceExamples from that file.
If left unspecified, the conversion from DB file is omited.
This file is part of my Master thesis.

Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

if [ "$1" == "-s" ]
    then
    if [ "${#2}" -ne 0 ] 
        then
        NOTESEQUENCEFILE=$(readlink -f $2)
        echo $NOTESEQUENCEFILE
        polyphony_rnn_create_dataset \
            --input="$NOTESEQUENCEFILE" \
            --output_dir=./tmp/polyphony_rnn/sequence_examples \
            --eval_ratio=0.10
        exit 1
    fi
    echo "NoteSequence file not specified!"
        echo "Script which will automatically prepare dataset for training neural network.
Prerequisite is to run scripts prerequisities.sh and install.sh
First argument is folder with MIDI files.
Second argument is the SQLite DB file with songs.

If first argument is -s and second path to the noteSequence file, 
then script will make only SequenceExamples from that file.
If left unspecified, the conversion from DB file is omited.
This file is part of my Master thesis.

Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi
echo "COntinue"
# get absolute path
MIDI=$(readlink -f $1)

#check if DB file was added
if [ "${#2}" -ne 0 ] 
    then
    #make output folder
    mkdir "$MIDI"
    # get absolute path
    DB=$(readlink -f $2)
    #run the conversion
    cd ./harmonizer
    python dbToMIDI.py "$DB" "$MIDI"
    cd ..
fi


#activate magenta virtual environment
source activate magenta

#convert midi files to note sequences
convert_dir_to_note_sequences \
    --input_dir="$MIDI" \
    --output_file=./tmp/notesequences.tfrecord \
    --recursive

# convert notesequences to sequence examples
polyphony_rnn_create_dataset \
    --input=./tmp/notesequences.tfrecord \
    --output_dir=./tmp/polyphony_rnn/sequence_examples \
    --eval_ratio=0.10

