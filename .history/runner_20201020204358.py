import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


from speech import recordCommandPyAudio, recordCommandSounddevice

if __name__ == "__main__": 
    # while True:
    rate = 44100
    command = recordCommandSounddevice()        
    print("Got command")
    sd.play(command, rate)
    sd.wait()