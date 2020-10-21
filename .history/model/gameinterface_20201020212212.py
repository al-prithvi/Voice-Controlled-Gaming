class GameInterface:
    
    def __init__(self):
        super().__init__()
        self.command1 = None
        self.command0 = None
    # Text based command

    def processCommand(self, command):
        if command == "left":
            if self.command1 == "go":
                # Keep going left

