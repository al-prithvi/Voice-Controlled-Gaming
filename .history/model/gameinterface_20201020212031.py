class GameInterface:
    
    def __init__(self):
        super().__init__()
        self.previousCommand = None
    
    # Text based command

    def processCommand(self, command):
        if command == "left":

