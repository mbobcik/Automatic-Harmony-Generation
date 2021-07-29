#!/bin/bash
# Script which will automatically start evaluation process of the neural network
# with hyper parameters provided in the thesis.
# it should run alongside with training process.
# First argument is run_dir, folder in which log files and neural network should be saved
# Second argument is path to sequenceExamples file with training data.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology

#check arguments
if [ -z "$1" ] 
    then
    echo "Run folder and SequenceExamples file not specified!"
    echo "Script which will automatically start evaluation process of the neural network
with hyper parameters provided in the thesis.
it should run alongside with training process.
First argument is run_dir, folder in which log files and neural network should be saved
Second argument is path to sequenceExamples file with training data.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

if [ -z "$2" ] 
    then
    echo "SequenceExamples file not specified!"
        echo "Script which will automatically start evaluation process of the neural network
with hyper parameters provided in the thesis.
it should run alongside with training process.
First argument is run_dir, folder in which log files and neural network should be saved
Second argument is path to sequenceExamples file with training data.
Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"

    exit 1
fi

RUNDIR=$(readlink -f $1)
SEFILE=$(readlink -f $2)

#run evaluation process
polyphony_rnn_train \
    --run_dir="$RUNDIR" \
    --sequence_example_file="$SEFILE" \
    --hparams="batch_size=64,rnn_layer_sizes=[64,64]" \
    --num_eval_examples=20000 \
    --eval