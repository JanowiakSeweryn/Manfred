import numpy as np
import librosa
import os
import json
import re
import random
import sys

N_FFT = 1024

# pattern=r""
def UpgradeModel():

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "upgrade_model":
            return True
        
    else:
        return False

def DefineModel():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        pattern = r"^/Models/manfred_v\d+(\.\d+)*\.pth$"

        if re.match(pattern,command):
            return command
        else:
            return "None"
    else:
        return "None"

UPDATE_MODEL = UpgradeModel()

LABELS = [
    "clap",
    "silence" ,
    "talk" ,
    "snap" ,
    "manfred",
    "spotify",
    "yhm",
    "night",
    "skip",
    "reconnect",
    "stop" ,
    "exit" ,
    "lockin" ,
    "back" ,
    "gaymini",
    "replay",
    "cp",
    "pogoda",
    "google",
    "terminal",
    "next" ,
    "readmsg",
    "party"
]

         

def get_indekses(LABELS):
    indekses = []
    for l in LABELS:
        indekses.append(0)
    return indekses

# INSTRUCTIONS = [x for x in LABELS if x!= "manfred" and x!="talk" ]

LCOUNTER = dict(zip(LABELS,get_indekses(LABELS=LABELS))) 

#ON Data augmentation is only for x_train, which is only the 
def spec_reverse(S_mel,sr=16000):

    S_inv = librosa.db_to_power(S_mel)
    y_reconstructed = librosa.feature.inverse.mel_to_audio(S_inv,n_fft=N_FFT,n_iter=64,hop_length=512)
    print(f"frames = {len(y_reconstructed)}")
    return y_reconstructed

def SaveData(features,labels,filename):

    data = {
    "features" : features.tolist(),
    "labels" : labels.tolist()
    }
    fn=f"{filename}.npz"

    np.savez(fn,**data)

    # with open(fn, "w") as f:
    #     # json.dump(data, f)

def LoadData(fn):

    Data = np.load(fn,allow_pickle=True)
    # with open(fn, "r") as f:
    #     Data = json.load(f)
    
    return Data

def ShuffleData(x,y):

    data = list(zip(x,y))
    random.shuffle(data)
    xs,ys = data
    return xs,ys


def split_data(input_data, target_data, train_size):


    test_size = round(len(input_data)*train_size)
    x_train = input_data[0:test_size]
    x_test = input_data[test_size:len(input_data)]

    y_train = target_data[0:test_size]
    y_test = target_data[test_size:len(input_data)]

    return x_train, y_train, x_test, y_test

def features_dict_to_vector(features):
    vector = []

    for key, value in features.items():
        # Ensure value is a numpy array
        value = np.asarray(value)
        
        # MFCC is 2D
        if key == "mfcc" or key=="mspec":
            a = 0
            # value shape: (n_mfcc, frames)
            # Get mean and std for each MFCC coefficient across time
            vector.extend(np.mean(value, axis=1).flatten())
            vector.extend(np.std(value, axis=1).flatten())

        # All other features are 1D arrays
        else:
            # Compute scalar statistics from the 1D array
            vector.append(float(np.mean(value)))
            vector.append(float(np.std(value)))

    return np.array(vector, dtype=np.float32)

def Normalize(S_dB):
    S_min = S_dB.min()
    S_max = S_dB.max()

    # Check for division by zero just in case the file is silent
    if S_max - S_min > 0:
        return (S_dB - S_min) / (S_max - S_min)
    else:
        return np.zeros_like(S_dB)

def extract_features(y,sr):

    # Avoid too-short signals
    # if len(y) < 2048:
    #     return None


    # mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    y = librosa.util.normalize(y)
    mspec = librosa.feature.melspectrogram(y=y,sr=sr,n_mels=64,n_fft=N_FFT,hop_length=512)


    # log_S = librosa.power_to_db(mspec,ref=np.max)

    log_S = librosa.power_to_db(mspec)

    # 3. Apply CMVN
    # We calculate mean/std along axis 1 (the time axis)
    mean = np.mean(log_S, axis=1, keepdims=True)
    std = np.std(log_S, axis=1, keepdims=True)

    # Add a tiny epsilon to prevent division by zero
    log_S_normalized = (log_S - mean) / (std + 1e-9)

    # delta = librosa.feature.delta(mfcc)
    # delta2 = librosa.feature.delta(mfcc, order=2)



    # features = {
    #     "energy": librosa.feature.rms(y=y)[0] ,                 # array
    #     "zrc": librosa.feature.zero_crossing_rate(y=y)[0],     # array
    #     "centroid": librosa.feature.spectral_centroid(y=y, sr=sr)[0],
    #     "bandwidth": librosa.feature.spectral_bandwidth(y=y, sr=sr)[0],
    #     "flux": librosa.onset.onset_strength(y=y, sr=sr),
    #     "mspec":mspec,
    #     "mfcc": mfcc,
    #     "delta1" : delta,
    #     "delta2" : delta2,
    # }

    # data1 = np.mean(mfcc,axis=1)
    # data = np.ndarray.tolist(data1)

    # data.append(energy)
     
    # features = data

    # data = mfcc[1]
    
    data = log_S_normalized
    # data = features_dict_to_vector(features=features)

    return data


def check_prev(current,prev,label):
    if current == prev and current == label:
        return True
    else:
        return False

def get_version(base="manfred",ext=".pth",):
    counter = 1
    counter_main = 1
    while os.path.exists(f"Models/{base}_v{counter_main}.{counter}{ext}" ):
        counter += 1
        if counter >= 10:
            counter = 1
            counter_main += 1
    
    model_name = DefineModel()
    if model_name != "None" and not UPDATE_MODEL:
        return f"Models/{model_name}"
    if UPDATE_MODEL:
        return f"Models/{base}_v{counter_main}.{counter}{ext}" 
    else :
        if counter - 1 == 0 and counter_main != 1:
            counter_main -= 1
        return f"Models/{base}_v{counter_main}.{counter-1}{ext}" 
    




