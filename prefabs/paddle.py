import flet



class Paddle (flet.Container):
    def __init__(self) -> None:
        super().__init__()
        self.bgcolor = "white"

        self.width = 50
        self.height = 150
    

    def move_up (self):
        self.top = self.top - 50
        self.update()

    
    def move_down (self):
        self.top = self.top + 50
        self.update()