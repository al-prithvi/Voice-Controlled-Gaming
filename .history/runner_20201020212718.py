import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


from CommandRecorder import recordCommandPyAudio, recordCommandSounddevice
from CommandRecognizer import Recognizer
from GameInterface import GameInterface

# yes, no, up, down, left, right, on, off, stop, go

if __name__ == "__main__": 

    recognizer = Recognizer()
    gameInterface = GameInterface()
    
    while True:
        command = recordCommandSounddevice(duration=2, playback=True)
