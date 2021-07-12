# Gestures to Bash

This repo attempts to use [mediapipe Hands-API](https://google.github.io/mediapipe/solutions/hands) to detect human gestures and execute Bash commands. The "proof of concept" is to accomplish a sci-fi kind of ux running "xdotool" in every gesture and navigate in a Linux interface. 

The project is made as a playground where you can parse static and moving gestures of your own and assign them any bash command you want (of course is a requirement to install anything you might want to use, such as xdotool). 

This can be done as follows:

`python moving_gesture_parser.py swipeleft xdotool key super+Left`

`python gesture_gesture_parser.py ok gnome-terminal`

Then running:

`python main.py`

you can try them out.


### Heres a video preview
https://user-images.githubusercontent.com/5643677/125218062-732a7200-e298-11eb-99cf-faece5805f0d.mov

