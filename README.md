# The Hypixel Dream game mode fetcher
## What?

Have you ever wanted to know what Hypixel Bedwars Dream-mode is active right now without having to actually log in to check?\
No more logging in and realising you don't want to actually play that one Gamemode only to immediately log out again!\
This tool provides this exact functionality and removes the need for a minecraft client!\
Enjoy the power of knowledge from the convenience of your Command-Line!\
In order to use it you need a Hypixel API key aswell as python3 and the requests library.

## tl;dr

- clone this repo
- run the main programm(it will generate a config file)
- enter your api-key into the config file (you can get it by running /api on hypixel)
- enjoy 🛌

## Installing


**Git**
```
git clone https://github.com/respinmo/hypixel_dream_mode_fetcher.git
```
**Dependencies**\
The only dependency is the Python requests package
```
pip3 install -r requirements.txt
```

alternatively (or if the command above doesn't work) just run:
```
python3 -m pip install requests
```

## Basic Usage

```
python3 bw_dream_fetch.py
```
Upon first time running the programm you will we asked, whether a config file should be created. Type in "y" and replace the "your_key" in the newly created
"config.ini" file with the 
api-key you have from hypixel(Get this Key by running /api on Hypixel).

You can also get additional information about how to use this tool by running 
```
python3 main.py --help
```
### Furthermore
---
🚀Due to popular request we decided to deactivate the Blockchain for this version.\
🚀Machine learning support coming soon!
