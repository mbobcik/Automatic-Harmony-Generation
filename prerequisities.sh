#!/bin/bash
# Script which will automatically install Magenta prerequisities .
# Prerequisite is to run script prerequisities.sh 
# inspired by https://raw.githubusercontent.com/tensorflow/magenta/master/magenta/tools/magenta-install.sh
# This file is part of my Master thesis.
#
# Author: Bc. Martin Bobčík, xbobci00
# Copyright (C) 2021 Brno University of Technology, Faculty of Information Technology



# install prerequisities
sudo apt-get update
sudo apt-get install build-essential libasound2-dev libjack-dev

#install conda
readonly MINICONDA_SCRIPT='Miniconda3-latest-Linux-x86_64.sh'
if [[ ! $(which conda) ]]; then
    readonly CONDA_INSTALL="/tmp/${MINICONDA_SCRIPT}"
    readonly CONDA_PREFIX="${HOME}/miniconda3"
    curl "https://repo.anaconda.com/miniconda/${MINICONDA_SCRIPT}" > "${CONDA_INSTALL}"
    bash "${CONDA_INSTALL}" -p "${CONDA_PREFIX}"
    export PATH="${CONDA_PREFIX}/bin:${PATH}"
    if [[ ! $(which conda) ]]; then
        err 'Could not find conda command. conda binary was not properly added to PATH'
    fi
fi

if [[ $(conda info --envs | grep "*" | awk '{print $1}') != "magenta" ]]; then
  #create virtual environment
  conda create -n magenta python=3.7
  
fi
