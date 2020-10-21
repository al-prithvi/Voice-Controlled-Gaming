import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


from speech import recordCommandPyAudio, recordCommandSounddevice

# yes, no, up, down, left, right, on, off, stop, go

if __name__ == "__main__": 
    while True:
        rate = 44100
        command = recordCommandPyAudio(duration=2, playback=True)