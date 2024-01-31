# Setup of Webserver & Code development on Raspberry
To work in save environment with easy package managment conda is being used. Therefore some speacial steps must be taken to install conda.

As always first update & upgrade package lists and assign ourselfs as admin:
```
sudo su
apt-get update && apt-get upgrade -y
```


## Venv & Dependencies Installation: 
The following steps have been taken to install the Virtual Environment, activate it and install Python packages. 
Python 3.10 should be installed as well. 
Please understand that the whole setup procedure might need adaption as packages, python and Raspian develop further. Therefore this is inteded to document the current setup and might not be suitable for reproduction in the future while also not beeing a complete guide since the Team had limited capacities.

Update pip:

Execute the following command to ensure that your pip is up to date:
```
python3 -m pip install --upgrade pip
```
Create a virtual environment:

Navigate to the directory where you want to store your project and create a virtual environment with the following command:
```
python3 -m venv venv
```
Activate the virtual environment:

Activate the virtual environment with the command:
```
source venv/bin/activate
```
Install Dash:

Use pip within the virtual environment to install Dash:
```
pip install dash dash_bootstrap_components flask pyserial
```
## Setup git to download & Update Code
First install git: 
```
apt-get install git
```

The Git repossitory has been cloned to /home/tee/ with 
```
git clone https://github.com/Energieseminar/Inselfitness.git
```
The Code from main branch is fetched by the following command:
```
git pull
```
Then the environment in which the libraries are installed must be actived with the below command:
```
source /home/tee/bin/activate
```
Perform Pythonscript:
```
python simple_app.py
```
## Setup Cronjob and respective bash script
This is to regulary update the running script which might be helpful when developing in such a restrictive Network environment as a Company or TU Berlin (:

# TODO: Write what has been done here
