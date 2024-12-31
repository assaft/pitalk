# pitalk
PiTalk is a peer-to-peer voice messanger running on Raspberry PI. PiTalk installation involes 1+N devices:
* First is the Admin machine
* Then there are N end-user devices for communicating with each other.

PiTalk was developed and tested on Raspberry PI Zero 2 W, however it is likely to work on other Pi versions. 

## Installation for Admin

### Create a Dropbox Application
You need to create a dropbox application that will serve for passing messages between users. The instructions below are based on [this)[https://pimylifeup.com/raspberry-pi-dropbox/] guide, with a few updates. You can use any computer to perform this step (not necessarily the Admin machine).
* Go to [Dropbox developers page](https://www.dropbox.com/developers/apps).
* Press on `Create app`
* Select `Scoped access` and then `App folder`
* Give a name to your app
* Press `Create app`
* You may want to change `App folder name`
* Store the `App key` and `App secret` for later use (press `show` if secret is hidden)
* Switch to the `Permissions` tab
* Under `Files and folders`, make sure both `read` and `write` are selected for `files.metadata` and `files.content`

### Software Installation
* Use the Raspberry PI Imager (tested with v1.8.5) to install Raspberry PI OS Lite (64-bit) on a Class 10 A1 32GB card (or better spec-ed). For easy access, pre-configure wifi + user: pitalk_admin.
* SSH into the pi:
```bash
ssh pitalk_admin@PI-IP
```
* Install pitalk and its dependencies. Note that this includes `Dropbox-Uploader`, which will ask for the `App key` and `App secret` mentioned above. It will also ask you to open a link in your web browser for creating an access token. 
```
sudo apt -y install git
git clone https://github.com/assaft/pitalk.git
cd pitalk
./scripts/install_admin.sh
```


### Create users
Repeat the process below for each user:
* Preapre a WAV file announcing the name of the user
* Select the user_name for the user
* Run:
```bash
python preprare/users/create_user.py <user_name> <full name> <path to wav file>
```
For example:
```bash
python preprare/users/create_user.py john_smith "John Smith" /home/pitalk/john_smith.wav
```
* Use the user name you selected when installing the Pi for this user.

### Delete user
Similar to above:
```bash
python preprare/users/delete_user.py <user_name>
```
For example:
```bash
python preprare/users/delete_user.py john_smith
```


### Create friendships
Repeat this process for each pair of users that will be communicating by voice messages:
```bash
python preprare/users/create_friendship.py <user_name1> <user_name2>
```
For example:
```bash
python preprare/users/create_friendship.py john_smith jane_doe
```

### Cancel friendships
As above:
```bash
python preprare/users/cancel_friendship.py <user_name1> <user_name2>
```
For example:
```bash
python preprare/users/cancel_friendship.py john_smith jane_doe
```


## Installation for end-users

### Hardware Installation

#### Hardware Requirements:
1. Raspberry PI Zero 2 W + Power adapter.
2. Amplifier Breakout - MAX98357A, such as [this](https://www.adafruit.com/product/3006).
3. Speaker 3W 4ohm, such as [this](https://www.amazon.com/gp/product/B096NGVHL2/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).
4. Microphone
5. Push Buttons: 3
6. Lights: 3
7. Enclosure

#### Hardware Installation:
* Start by connecting the amplifier + speaker to the Pi as explained [here](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-wiring). Notice the table of contents on the left hand side to jump to other sections.
* Connect the microphone to the Pi
* Connect the buttons + lights to the Pi
* Attach everything in the Enclosure

### Software Installation
* Use the Raspberry PI Imager (tested with v1.8.5) to install Raspberry PI OS Lite (64-bit) on a Class 10 A1 32GB card (or better spec-ed). For easy access, pre-configure wifi + user (pitalk).
* SSH into the pi:
```bash
ssh pitalk@PI-IP
```
* Install pitalk and its dependencies. This process includes some interactive steps:
    * `Dropbox-Uploader` will ask for the `App key` and `App secret` mentioned above. It will also ask you to open a link in your web browser for creating an access token. 
    * You will be asked to enter the `user name` and `full name` for the user, and to provide a path to a WAV file announcing his/her name.
```bash
sudo apt -y install git
git clone https://github.com/assaft/pitalk.git
cd pitalk
./scripts/install_user.sh
```
* At the end of this process, you will be given a path to an RSA public key that was created for this user.
 


## I2S Audio

Follow this tutorial:
* By [Adafruit](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-wiring), notice the table of contents on the left hand side to jump to other sections.

Note that [this](https://www.lucadentella.it/en/2017/04/26/raspberry-pi-zero-audio-output-via-i2s/) is not up-to-date, and contains a mistake: instead of PIN18, 19, 21, it needs to be GPIO 18, 19, 21. Adafruit got it right [here](https://learn.adafruit.com/assets/37880).



PITALK_HOME = ~/pitalk
DROPBOX_HOME = ~/dropbox

Step 1 - on user hardware:
A. create a new user by the python script

PITALK_HOME:
             /prepare
                /user_x
                    /keys
                        /rsa_private.txt
                        /rsa_public.txt
                    /card
                        /user_x.json
             /src/pitalk
             ...

B. copy/add the user pubic key and card to dropbox 

DROPBOX_HOME:
            /users
                /user_x
                    /keys
                        /rsa_public.txt
                    /card
                        /user_x.json

Step 2 - On the Admin hardware:

A. Sync to the most up-to-date users directory:

DROPBOX_HOME:
            /users
                /user_x
                    /keys
                        /rsa_public.txt
                    /card
                        /user_x.json
                /user_y
                    /keys
                        /rsa_public.txt
                    /card
                        /user_y.json
                /user_z
                    /keys
                        /rsa_public.txt
                    /card
                        /user_z.json

B. Add friend cards to create friendships:
            /users
                /user_x
                    /keys
                        /rsa_public.txt
                    /card
                        /user_x.json
                    /friends
                        /user_y.json
                        /user_z.json
                /user_y
                    /keys
                        /rsa_public.txt
                    /card
                        /user_y.json
                    /friends 
                        /user_x.json           
                /user_z
                    /keys
                        /rsa_public.txt
                    /card
                        /user_z.json
                    /friends 
                        /user_x.json           


Stage 3 - Back on the user hardware:

Run pitalk

It will sync on the friends list for the active user
It will let you send messages to its friends
It will play messages you receive from friends
