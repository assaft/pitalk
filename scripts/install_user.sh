#!/bin/bash
set -e

# os updates
sudo apt update -y
sudo apt upgrade -y

# install python, portaudio and dropbox
scripts/install_python.sh
scripts/install_portaudio.sh
scripts/install_dropbox.sh

# settings
echo "export PITALK_HOME=~/pitalk" >> ~/.bashrc
echo "export DROPBOX_HOME=~/dropbox" >> ~/.bashrc
echo "export DROPBOX_UPLOADER_HOME=~/Dropbox-Uploader" >> ~/.bashrc
source ~/.bashrc

# install pitalk
scripts/install_pitalk.sh
