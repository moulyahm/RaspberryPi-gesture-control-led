# Gesture Controlled LED using Raspberry Pi

## Description
This project uses hand gesture recognition to control LEDs connected to a Raspberry Pi in real-time.

## Objective
To implement a touchless control system using computer vision and embedded GPIO.

## Hardware Required
* Raspberry Pi 4
* USB Camera / Pi Camera
* 2 LEDs
* Resistors (220Ω)
* Breadboard & jumper wires

## Software Used
* Python 3
* OpenCV
* MediaPipe
* RPi.GPIO

## Installation
```bash
sudo apt update
sudo apt install python3-pip
pip3 install opencv-python mediapipe RPi.GPIO
```

## Run the Project
```bash
python3 src/gesture_control.py
```

## 🔌 GPIO Connections
* LED1 → GPIO 23
* LED2 → GPIO 24
* GND → Resistors → LEDs

## 🧠 Working
* Detects hand using MediaPipe
* Identifies finger positions
* Recognizes gestures:
* ONE → LED1 ON
* PEACE → LED2 ON
* Other gestures → LEDs OFF

## 🚀 Future Improvements
* Control multiple appliances
* Add voice + gesture hybrid system
* Integrate IoT dashboard
* Optimize using Edge AI models



