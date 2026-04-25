# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
#  ------------------- FUNCTIONS AND TASK OF MANFRED ----------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

import time
import subprocess
import librosa
import sounddevice as sd
import os
import random

CURRENT_DIR = os.getcwd()

manfred_allert, fs2 = librosa.load(f"{CURRENT_DIR}/sounds/manfredv11.wav",sr=16000)

def SoundManfred(audio=manfred_allert,fs=16000):
    print("sigma")
    sd.play(audio,fs)

#open spotify and play specific playlist
def OpenSpotify(PLAYLIST_URI = "spotify:playlist:5LZB4GDKZVq24Z6W270PZ3"):

    # subprocess.run("connect_jbl.sh")
    # Start Spotify (does nothing if already running)
    subprocess.Popen(["spotify"])

    # Give Spotify time to start
    time.sleep(2.5)

    # Open playlist and PLAY
    subprocess.run([
        "playerctl",
        "-p", "spotify",
        "open",
        PLAYLIST_URI
    ])

def OpenGaymini():
    subprocess.run(["google-chrome" , "https://gemini.google.com/app?hl=pl"])

    time.sleep(0.5)

    subprocess.run(["wmctrl","-a","Google Chrome"])

def CloseChromeTab():
    commands = ["xdotool", "search", "--onlyvisible", 
    "--class" ,"google-chrome" ,"windowactivate" ,
    "--sync" ,"key", "ctrl+w"]

    subprocess.run(commands)

def Chillstep():

    
    PLAYLIST_URI = "spotify:playlist:5HOitcztsmc74UHgbKfwfn?si=42f7ee2d9dbd4dfd"
    # Start Spotify (does nothing if already running
    subprocess.Popen(["spotify"])

    # Give Spotify time to start
    time.sleep(2.5)

    # Open playlist and PLAY
    subprocess.run([
        "playerctl",
        "-p", "spotify",
        "open",
        PLAYLIST_URI
    ])

# connect to JBL GO devices 
def Reconnect():
    subprocess.run(["bluetoothctl","connect","78:44:05:83:CB:F9"])

def OpenYtPlaylist():
    # playlist = ["https://www.youtube.com/watch?v=PRyVBv8T2s4&list=RDPRyVBv8T2s4",
    # "https://www.youtube.com/watch?v=ncHWcgju-eo&list=RDncHWcgju-eo"]
    # iter = random.randint(0,len(playlist)-1)
    playlist = "https://www.youtube.com/watch?v=2VXXa_x8pBs&list=PLiS1TsEprqAo34rbDEZoOC-De_zgxsTiK"
    subprocess.run(["google-chrome",playlist])

#skip the annooying song to the next in the playlist
def PlayNext():
    subprocess.run(["playerctl", "next"])

def CheckWeather():
    subprocess.run(["google-chrome", "google.com/search?q=pogoda kraków"])

#stops and start playing whenever was not and paused
def StopMusic():
    subprocess.run(["playerctl",  "play-pause"])

def KillSpotify():
    subprocess.run(["playerctl", "-p", "spotify", "quit"], check=False)

    subprocess.run(["pkill", "spotify"])

def PlayBack():
    subprocess.run(["playerctl", "previous"])
    subprocess.run(["playerctl", "previous"])

def KillManfred():
    exit()

#change_view.sh -> errors h&d
def ChangeViewGoogle(tab_name="Google Chrome"):
    subprocess.run(["sh","change_view.sh",tab_name])

def ChangeViewTable():
    tab_name="\"Terminal\"" 
    ChangeViewGoogle(tab_name=tab_name)


def OpenFunnyBox():
    subprocess.run(["google-chrome" , "https://www.youtube.com/shorts/lUuueVIRL2U"])

    time.sleep(0.5)

    subprocess.run(["wmctrl","-a","Google Chrome"])

def Replay():
    subprocess.run(["playerctl", "-p", "spotify", "previous"])




# --------------------------------------------------------------------
# ---------------------------MAIN TASKS LIST -------------------------
# --------------------------------------------------------------------
TASKS = {
    "spotify" : OpenSpotify,
    "reconnect" : Reconnect,
    "skip": PlayNext,
    "back" :PlayBack,
    "stop" : StopMusic,
    "exit": KillSpotify,
    "clap" : KillManfred,
    # "lockin" : Chillstep,
    "lockin" : OpenYtPlaylist,

    "gaymini" : OpenGaymini,
    "cp" : OpenFunnyBox,
    "pogoda": CheckWeather,
    "replay" : Replay,
    "party" : OpenYtPlaylist,
    "google" : ChangeViewGoogle, #-- > need to modify the "changeView.sh" script
    "Terminal": ChangeViewTable
}

class Task:
    def __init__(self,task):
        self.taskname = task
        self.checked = False
        self.iter = 0

    def count(self,limits):
        self.iter += 1
        if self.iter > limits:
            self.checked = True
    
    def DoTask(self):
        if self.checked:
            TASKS[self.taskname]()
            self.checked = False
            self.iter = 0

def get_list():
    task_list = []
    for t in TASKS.keys():
        task_list.append(Task(t))
    return task_list

TASK_LIST = get_list()


 
