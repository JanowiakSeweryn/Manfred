# Manfred16

Manfred is a gesture and voice-controlled assistant designed to make system tasks easier. It uses a CNN-based model to recognize inputs and trigger specific actions.

## Features

Manfred can handle several tasks through simple commands or gestures:
- **Music control**: Open Spotify, skip tracks, go back, or pause music.
- **Web Browsing**: Open Gemini (for assistant tasks), check the weather, or open specific YouTube playlists.
- **System actions**: Reconnect Bluetooth devices (like JBL speakers), switch between active windows (Chrome/Terminal), or kill specific processes.
- **Fun stuff**: There is even a shortcut for quick YouTube shorts.

## How it's built

The project is split into a few main parts:
1. **The Brain**: A Convolutional Neural Network (CNN) implemented in Python (using Torch) that handles the recognition logic.
2. **The Server**: A C++ backend (`server.cpp`) that manages communication.
3. **The Interface**: A GUI built with SDL2 (`window.py`) and a simple web-based control panel (`index.html`).
4. **Task Runner**: `task.py` contains the logic for all the automated actions Manfred can perform.

## Setup

- Ensure you have the dependencies from `requiments.txt` installed.
- The project uses `librosa` and `sounddevice` for audio handling, and `sdl2` for the window interface.
- You can train the model using `train.py` if you have your dataset ready in `DATASET.npz`.
