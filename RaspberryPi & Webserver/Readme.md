# Setup of Webserver & Code development on Raspberry
To work in save environment with easy package managment conda is being used. Therefore some speacial steps must be taken to install conda.
## Conda Installation: 

We followed the instructions of a well done Stackoverflow Question:
*Note: The added environment is named "streamlit" like the webserrver app*

Installing Miniconda on Raspberry Pi and adding Python 3.5 / 3.6
Skip the first section if you have already installed Miniconda successfully.

Installation of Miniconda on Raspberry Pi

```
wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
sudo md5sum Miniconda3-latest-Linux-armv7l.sh
sudo /bin/bash Miniconda3-latest-Linux-armv7l.sh
```
Accept the license agreement with **yes**

When asked, change the install location: **/home/pi/miniconda3**

Do you wish the installer to prepend the Miniconda3 install location to PATH in your /root/.bashrc ? **yes**

Now add the install path to the PATH variable:

```
sudo nano /home/pi/.bashrc
```

Go to the end of the file .bashrc and add the following line:
```
export PATH="/home/pi/miniconda3/bin:$PATH"
```

Save the file and exit.

To test if the installation was successful, open a new terminal and enter
```
conda
```
If you see a list with commands you are ready to go.

----------------------------
But how can you use Python versions greater than 3.4 ?

Adding Python 3.5 / 3.6 to Miniconda on Raspberry Pi

After the installation of Miniconda I could not yet install Python versions higher than Python 3.4, but i needed Python 3.5. Here is the solution which worked for me on my Raspberry Pi 4:

First i added the Berryconda package manager by jjhelmus (kind of an up-to-date version of the armv7l version of Miniconda):
```
conda config --add channels rpi
```
Only now I was able to install Python 3.5 or 3.6 without the need for compiling it myself:
```
conda install python=3.5
conda install python=3.6
```
Afterwards I was able to create environments with the added Python version, e.g. with Python 3.5:
```
conda create --name py35 python=3.5
```
The new environment "py35" can now be activated:
```
source activate py35
```
Using Python 3.7 on Raspberry Pi

Currently Jonathan Helmus, who is the developer of berryconda, is working on adding Python 3.7 support, if you want to see if there is an update or if you want to support him, have a look at this pull request. (update 20200623) berryconda is now inactive, This project is no longer active, no recipe will be updated and no packages will be added to the rpi channel. If you need to run Python 3.7 on your Pi right now, you can do so without Miniconda. Check if you are running the latest version of Raspbian OS called Buster. Buster ships with Python 3.7 preinstalled (source), so simply run your program with the following command:

Python3.7 app-that-needs-python37.py

I hope this solution will work for you too!

Antwort von Paul Strobel von Stack Overflow

## Setup git to download & Update Code

