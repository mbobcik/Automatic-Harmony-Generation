#!/bin/bash
# Script which will generate 10 harmonized files based on 
# specified MIDI file with melody.

# First argument specifies path to bundle file of model
# Second argument specifies path to MIDI file.
# Third argument specifies number of measures in the MIDI file
# Last argument is temperature, which is optional.
# Default value is 1.0
# This file is part of my Master thesis.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology

if [ -z "$1" ] 
    then
    echo "Bundle file with model not specified!"
    echo "Script which will generate 10 harmonized files based on 
specified MIDI file with melody.

First argument specifies path to bundle file of model
Second argument specifies path to MIDI file.
Third argument specifies number of measures in the MIDI file
Last argument is temperature, which is optional.
Default value is 1.0
This file is part of my Master thesis.

Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    
    exit 1
fi

if [ -z "$2" ] 
    then
    echo "MIDI file with melody not specified!"
    echo "Script which will generate 10 harmonized files based on 
specified MIDI file with melody.

First argument specifies path to bundle file of model
Second argument specifies path to MIDI file.
Third argument specifies number of measures in the MIDI file
Last argument is temperature, which is optional.
Default value is 1.0
This file is part of my Master thesis.

Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

if [ -z "$3" ] 
    then
    echo "Script which will generate 10 harmonized files based on 
specified MIDI file with melody.

First argument specifies path to bundle file of model
Second argument specifies path to MIDI file.
Third argument specifies number of measures in the MIDI file
Last argument is temperature, which is optional.
Default value is 1.0
This file is part of my Master thesis.

Author: Bc. Martin Bobčík, xbobci00
Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology"
    exit 1
fi

TEMP=$4
if [ -z "$4" ] 
    then
    TEMP=1.0
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
    --inject_primer_during_generation=true \
    --temperature="$TEMP"    