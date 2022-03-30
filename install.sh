#!/usr/bin/env bash

# ENVIRONMENT SETUP

initEnv() {
    echo -e "\e[36m \e[1m [01] Installing Miniconda \e[0m"
    apt-get install wget
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p ~/miniconda 
    rm ~/miniconda.sh

    export PATH=~/miniconda/bin:$PATH

    echo -e "\e[36m \e[1m [02] Creating Conda Env \e[0m"
    conda env create -f virtualnet.yml
}

initEnv