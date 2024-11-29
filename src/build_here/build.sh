#!/bin/bash

pyinstaller --onefile --icon="../Dino.ico" --name="PRM" \
    --add-data="../about.txt:." \
    ../main.py

#note : ":." in "about.txt:." is package in the same location as the executable file