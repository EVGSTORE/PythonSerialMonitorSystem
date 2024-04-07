# PythonSerialMonitorSystem
This custom, yet underkill overkill app lets you select active com ports and send and watch commands from them. It also has a built-in audio file for NSL airsoft sounds

# This Python system contains:
* Dropdown Com port menu 
* Interface to see the most recent command received
* Textbox to send command to com port (also sends command back into the script virtually)
* Built-in 5 audio files (horn, buzzer, feet, weapon, and endgame) for NSL airsoft sound effects.
* Code for Arduino

# Python Info
How to compile:
* <code>pyinstaller --onefile --noconsole --add-data "boot.wav;." --add-data "buzzer.wav;." --add-data "endgame.wav;." --add-data "feet.wav;." --add-data "horn.wav;." --add-data "weapon.wav;." --add-data "templates;templates" app.py</code>

Dependents:
* webview, threading, serial, serial.tools.list_ports, pygame, queue, sys, os


# Preview
![evgcomportpreview](https://github.com/EVGSTORE/PythonSerialMonitorSystem/assets/58867183/7b9a9d9b-cbaf-416f-9043-fcfd40472c16)

# Disclaimer:
* This was built using w3css, python, javascript, HTML, and through limited use with AI generation such as ChatGPT 4
