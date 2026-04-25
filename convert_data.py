import librosa
import json 
import numpy as np
from pathlib import Path
from utility import features_dict_to_vector,LABELS,extract_features
import random


FILENAME = "DATASET.npz"

sample_rate = 16000

# Augmentation parameters
AUGMENTATION_ENABLED = True
AUGMENTATIONS_PER_SAMPLE = 25 # Number of augmented versions per original sample

TRAIN_SIZE = 0.3
TEST_SIZE = 0.35
VAL_SIZE = 0.35

def add_noise(audio, noise_factor=0.002):
    """Add white noise to audio signal"""
    noise = np.random.randn(len(audio))
    augmented = audio + noise_factor * noise
    return augmented


def pitch_shift(audio, sr, n_steps=0):
    """Shift pitch without changing speed"""
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)


def change_volume(audio, factor=1):
    """Change volume of audio"""
    return audio * factor

#if strech < 1 -> slows down,
#if strech > 1 -> speed up

def change_speed(audio,sr=sample_rate,strech=1.2):
    
    y = librosa.effects.time_stretch(audio,rate=strech)
    y1s = librosa.util.fix_length(y, size=sr)
    
    return y1s
    
def augment_audio(audio, sr):
    augmentation_type = np.random.choice(['pitch_shift', 'volume','speeddown'])
    
    if augmentation_type == 'noise':
        return add_noise(audio, noise_factor=np.random.uniform(-0.002, 0.005))
    
    elif augmentation_type == 'pitch_shift':
        n_steps = np.random.randint(-4,4)
        return pitch_shift(audio, sr, n_steps=n_steps)
    
    elif augmentation_type == 'volume':
        factor = np.random.uniform(0.4, 1.3)
        return change_volume(audio, factor=factor)

    elif augmentation_type == 'speeddown':
        factor = np.random.uniform(0.75, 1.25)
        return change_speed(audio=audio,sr=sr,strech=factor)

    return audio


def ConvertData():
    data_features = []
    data_label = []

    data = []

    # Define the root directory
    base_path = Path('Data')

    x_train = [] 
    x_val = []
    x_test = []

    y_train = [] 
    y_val = []
    y_test = []    

    if AUGMENTATION_ENABLED:
        print(" --- DATA AUGMENATION ANABLED --- ")

    for labels in LABELS:

        folder_path = Path(f"Data/{labels}")
        files = [f for f in folder_path.iterdir()]
        random.shuffle(files)

        # Convert the generator to a list to get the count
        file_count = len(list(folder_path.glob("*.wav")))

        iter = 0

        train_size = int(file_count*TRAIN_SIZE)
        test_size = int(file_count*TEST_SIZE)
        val_size = int(file_count*VAL_SIZE)

        print(f"{labels} class converting .")
        print(f"TRAIN,VAL,TEST: {train_size},{val_size},{test_size}")

        for file in files:

            y, sr = librosa.load(file, sr=sample_rate) 
            lf = librosa.feature

            data = extract_features(y=y,sr=sr)


            #data augmentation:

            if iter <= train_size:
                x_train.append(data.copy())
                y_train.append(labels)
                if AUGMENTATION_ENABLED:
                    for ag in range(AUGMENTATIONS_PER_SAMPLE):
                        y_ag = augment_audio(y,sr=sr)
                        data = extract_features(y=y_ag,sr=sr)
                        x_train.append(data.copy())
                        y_train.append(labels)
            elif iter > train_size and iter <= train_size + val_size:
                x_val.append(data.copy())
                y_val.append(labels)
            elif iter > val_size+train_size:
                x_test.append(data.copy())
                y_test.append(labels)
            iter += 1


    print(f"train:{len(x_train)},val:{len(x_val)},test:{len(x_test)}")

    Data = {
        "x_train" : x_train,
        "y_train" : y_train,
        "x_val" : x_val,
        "y_val" : y_val,
        "x_test": x_test,
        "y_test": y_test
    }

    np.savez(FILENAME,**Data,allow_pickle=True)

    print("data saved succesfully")

if __name__ == "__main__":
    ConvertData()

