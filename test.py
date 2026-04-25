import sounddevice as sd
import queue
import numpy as np
import joblib
from utility import extract_features,LABELS,check_prev
from task import TASK_LIST,SoundManfred
from window import Win

import subprocess

import os
from CNN import Net,MODEL_NAME
import torch
from collections import deque,Counter

import subprocess
import time
import sys
import threading


PRINT_LABEL = True
#5 signals are taking into when selecting final output 
SIGNAL_LIMIT = 7
#
Outputs_list = deque(maxlen=SIGNAL_LIMIT)

current_command = "None"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(BASE_DIR, "work.sh")

fs = 16000
channels = 1
blocksize = 640

# buffer = np.zeros((fs,channels))\
buffer = np.zeros(fs, dtype=np.float32)

audio_buffer = deque(maxlen=fs)

audio_q = queue.Queue()

#load model

print(f"loading the {MODEL_NAME}")
# net = Net()
# net.load_state_dict(torch.load(MODEL_NAME,map_location="cpu"))
# net.eval()

device = torch.device("cpu")
net = Net().to(device)

state_dict = torch.load(MODEL_NAME, map_location=device)
net.load_state_dict(state_dict)

net.eval()

# data = joblib.load("svm.joblib")
# clf = data["model"]

print(" ---------------------------------- ")
print(" -- succesfully loaded model  -- ")
print(f" -- {MODEL_NAME} -- ")
print(" ---------------------------------- ")


def audio_callback(indata, frames, time, status):
    global audio_q

    if status:
        print(status)
    audio_q.put(indata.copy())

index = 0
manfred_frames = 0 #time to give response or else manfred will be canceled
manfred_frames_limit = 80
manfred_frames_enable = 40
manfred_sound_limit = 20
manfred = False
manfred_enabled = False
manfred_play = False


def play_alert(sound_data):
    sd.play(sound_data, fs)

with sd.InputStream(
    samplerate=fs,
    channels=channels,
    blocksize=blocksize,
    callback=audio_callback

):
    window = Win()
    print("Listening...")
    idx = 0
    idx_manfred = 0
    #number of frames to make the prediction stop for a second
    frames_reset = 60
    frames_pred = 0
    pause_predict = False
    prev_label = "NONE"
    allert_sound = True
    prev_radious = 0

    while True:
        if not window.run:
            break
        
        window.Events()
        window.Render_start()

        #give time to manfred if manfred didn't receive command then it exit :) 
        if manfred:
            manfred_frames+=1
            if manfred_frames > manfred_frames_limit:
                manfred = False
                manfred_enabled = False
                manfred_frames = 0
                allert_sound = True
                
                print("manfred turn off")
            if manfred_frames >= manfred_frames_enable and not manfred_enabled:
                manfred_enabled = True
            if manfred_frames >= manfred_frames_enable - manfred_sound_limit and not manfred_enabled:
                if allert_sound:
                    threading.Thread(target=SoundManfred, daemon=True).start()
                    allert_sound = False
        else:
            manfred_frames = 0
            allert_sound = True
        
        block = audio_q.get()
        n = len(block)

        # Slide buffer left
        buffer[:-n] = buffer[n:]
        # Append new samples at the end
        buffer[-n:] = block[:, 0]
        features = extract_features(buffer, fs)

        # print(f"number of features:{len(features)*len(features[0])}")

        # --- clasify --- ## 


        if features is not None and window.manfred_on:
            # features = Mel-spectrogram of shape [128, 87]
            x = torch.tensor(features, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # [1,1,128,87]
            with torch.no_grad():
                output = net(x)
                predicted_idx = output.argmax(dim=1).item()
                predicted_label = LABELS[predicted_idx]
            if PRINT_LABEL:
                if predicted_label != "talk" and predicted_label != "silence":
                    print(predicted_label)  

            if check_prev(predicted_label,prev_label,"manfred"):
                index += 1
            else:
                index = 0
            
            if index >= SIGNAL_LIMIT and not manfred:
                index = 0
                manfred = True

            if manfred_enabled:

                print("manfred is waiting for task")
                for task in TASK_LIST:
                    if check_prev(predicted_label,prev_label,task.taskname):
                        task.count(SIGNAL_LIMIT)
                    else:
                        task.iter = 0
                    if task.checked:
                        print(f"{predicted_label} work is DOING")
                        task.DoTask()
                        manfred = False
                        manfred_enabled = False
                        break
            else:
                for task in TASK_LIST:
                    task.iter = 0

            prev_label = predicted_label
            radious_mean = np.log(np.nanmax(block)+1e-6)*12 + 40
            # print(prev_radious, radious_mean)
            window.Draw(radious=radious_mean,prev_radious=prev_radious)
            prev_radious = radious_mean
    

            
        else:
            print("Signal too short for feature extraction")
            
            buffer = np.roll(buffer,-n)
        
        window.DrawButtons()
        window.Render_present()
        window.Reset_Events()

        

    window.Destroy()




