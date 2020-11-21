import time
# from pykeyboard import PyKeyboard
import keyboard
import time

def pressKey(command):
        
    valid_commands = ["left", "right", "up", "down"]
    if command in valid_commands:
        keyboard.press(command)
        time.sleep(1.5)
        keyboard.release(command)
 
    elif command == "go":
        keyboard.press("right+up")
        time.sleep(1.5)
        keyboard.release("right+up")
    elif command == "stop":
        keyboard.press("left+up")
        time.sleep(1.5)
        keyboard.release("left+up")

  