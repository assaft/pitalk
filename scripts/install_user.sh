# os updates
sudo apt update -y
sudo apt upgrade -y

# install python, portaudio and dropbox
scripts/install_python.sh
scripts/install_portaudio.sh
scripts/install_dropbox.sh

# settings
echo "export PITALK_HOME=~/pitalk" >> .bashrc
echo "export DROPBOX_HOME=~/dropbox" >> .bashrc

