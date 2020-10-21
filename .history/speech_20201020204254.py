
import pyaudio
import wave

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav


# https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python

def recordCommandPyAudio(duration = 3):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = duration
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return wf

def recordCommandSounddevice(duration = 3):
    fs=44100
    command = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete , Play Audio")
    # sd.play(command, fs)
    # sd.wait()
    # print("Play Audio Complete")

    return command