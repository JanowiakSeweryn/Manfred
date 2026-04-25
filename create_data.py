import sounddevice as sd
import soundfile as sf
import time
import os

SIGNAL_NAME = "reconnect"
CURRENT_SAMPLES = 1
SAMPLES_TO_RECORD = 200

DELAY = 0.1 # time in s between each sample

fs = 16000 #16khz
sd.default.samplerate = fs
sd.default.channels = 2

time.sleep(3)

newpath = f"Data/{SIGNAL_NAME}"

if not os.path.exists(newpath):
    os.makedirs(newpath)
else:
    if CURRENT_SAMPLES == 0 :
        print(f"Error: signal {SIGNAL_NAME} have some samples at {newpath}\n")
        print("change SIGNAL_NAME , or make sure to save changes before executing !!")
        exit()

#save 100 cklass
for i in range(CURRENT_SAMPLES,SAMPLES_TO_RECORD+CURRENT_SAMPLES):

    time.sleep(DELAY)
    #number of second as samples
    duration = 1
    print("record")
    myrecording = sd.rec(int(duration * fs))
    #wait to save file
    sd.wait()
    filename = f"Data/{SIGNAL_NAME}/{SIGNAL_NAME}sample{i}.wav"
    sf.write(filename, myrecording, fs)
    print(f"{i} sample recorded at {filename}")



