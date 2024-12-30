# pitalk
PiTalk is a peer-to-peer voice messanger running on Raspberry PI. PiTalk installation involes 1+N devices:
* First is the Admin machine
* Then there are N end-user devices for communicating with each other.

PiTalk was developed and tested on Raspberry PI Zero 2 W, however it is likely to work on other Pi versions. 



## Installation for Admin

### Software Installation
* Use the Raspberry PI Imager (tested with v1.8.5) to install Raspberry PI OS Lite (64-bit) on a Class 10 A1 32GB card (or better spec-ed). For easy access, pre-configure wifi + user: pitalk_admin.
* ssh pitalk_admin@1<ip>
* sudo apt -y install git
* git clone https://github.com/assaft/pitalk.git
* cd pitalk
* ./scripts/install_admin.sh

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


* Define friendships


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
* ssh pitalk@1<ip>
* sudo apt -y install git
* git clone https://github.com/assaft/pitalk.git
* cd pitalk
* ./scripts/install_user.sh

## I2S Audio

Follow this tutorial:
* By [Adafruit](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-wiring), notice the table of contents on the left hand side to jump to other sections.

Note that [this](https://www.lucadentella.it/en/2017/04/26/raspberry-pi-zero-audio-output-via-i2s/) is not up-to-date, and contains a mistake: instead of PIN18, 19, 21, it needs to be GPIO 18, 19, 21. Adafruit got it right [here](https://learn.adafruit.com/assets/37880).
