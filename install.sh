#!/bin/bash
# Script which will automatically install Magenta into conda virtual environment
# inspired by https://raw.githubusercontent.com/tensorflow/magenta/master/magenta/tools/magenta-install.sh
# This file is part of my Master thesis.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology




conda activate magenta
if [[ $(conda info --envs | grep "*" | awk '{print $1}') != "magenta" ]]; then
  err 'Did not successfully activate the magenta conda environment'
fi
# install pip packages
pip install -r requirements.txt