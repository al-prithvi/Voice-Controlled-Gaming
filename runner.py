from CommandRecorder import recordCommandPyAudio, recordCommandSounddevice
from CommandRecognizer import Recognizer
from GameInterface import GameInterface

# yes, no, up, down, left, right, on, off, stop, go

if __name__ == "__main__":

    recognizer = Recognizer()
    gameInterface = GameInterface()

    while True:
        command = recordCommandSounddevice(duration=1.5, playback=False) # 1500
        command = recognizer.classifyCommand(command)
        gameInterface.processCommand(command)