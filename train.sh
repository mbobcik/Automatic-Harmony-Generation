#!/bin/bash
# Script which will automatically train the neural network
# with hyper parameters provided in the thesis.
# Script will bundle the network afterwards
# First argument is run_dir, folder in which log files and neural network should be saved
# Second argument is path to sequenceExamples file with training data.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology

# check arguments
if [ -z "$1" ] 
    then
    echo "Run folder and SequenceExamples file not specified!"
    echo "Script which will automatically train the neural network
with hyper parameters provided in the thesis.
Script will bundle the network afterwards
First argument is run_dir, folder in which log files and neural network should be saved
Second argument is path to sequenceExamples file with training data.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

if [ -z "$2" ] 
    then
    echo "SequenceExamples file not specified!"
        echo "Script which will automatically train the neural network
with hyper parameters provided in the thesis.
Script will bundle the network afterwards
First argument is run_dir, folder in which log files and neural network should be saved
Second argument is path to sequenceExamples file with training data.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

RUNDIR=$(readlink -f $1)
SEFILE=$(readlink -f $2)

#train model
polyphony_rnn_train \
    --run_dir="$RUNDIR" \
    --sequence_example_file="$SEFILE" \
    --hparams="batch_size=64,rnn_layer_sizes=[64,64]" \
    --num_training_steps=20000

# pack model into bundle file
polyphony_rnn_generate \
    --run_dir="$RUNDIR" \
    --hparams="batch_size=64,rnn_layer_sizes=[64,64]" \
    --bundle_file="$RUNDIR"/polyphony_rnn.mag \
    --save_generator_bundle