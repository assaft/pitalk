#!/bin/bash
set -u

cd $DROPBOX_UPLOADER_PARENT_DIR
rm -Rf Dropbox-Uploader
git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
cd Dropbox-Uploader

./dropbox_uploader

#rm -f ~/.dropbox_uploader
#echo "CONFIGFILE_VERSION=2.0" >> ~/.dropbox_uploader
#echo "OAUTH_APP_KEY=${DROPBOX_APP_KEY}" >> ~/.dropbox_uploader
#echo "OAUTH_APP_SECRET=${DROPBOX_APP_SECRET}" >> ~/.dropbox_uploader
#echo "OAUTH_REFRESH_TOKEN=${DROPBOX_APP_TOKEN}" >> ~/.dropbox_uploader

DROPBOX_USER_NAME=$(./dropbox_uploader.sh info | grep "Name")
if [[ $DROPBOX_USER_NAME == *"Assaf Toledo"* ]]; then
  echo "Dropbox connection established."
else
  echo "Failed to connect to Dropbox"
  exit 1
fi
