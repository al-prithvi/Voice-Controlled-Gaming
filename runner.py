import time

from CommandRecorder import recordCommandPyAudio, recordCommandSounddevice
from CommandRecognizer import Recognizer
from GameInterface import GameInterface

# yes, no, up, down, left, right, on, off, stop, go

if __name__ == "__main__":

    recognizer = Recognizer()
    gameInterface = GameInterface()

    while True:
        start_time = time.time()
        command = recordCommandSounddevice(duration=1.5, playback=False) # 1500
        command = recognizer.classifyCommand(command)
        end_time = time.time()
        command_input_delay = (end_time - start_time)
        print('Command input delay: {:0.4f}s'.format(command_input_delay))
        gameInterface.processCommand(command)

        print()