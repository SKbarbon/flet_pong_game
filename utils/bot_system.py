import time, random

class BotMovementSystem:
    def __init__(self, main_class) -> None:
        self.main_class = main_class

    def movement(self):
        while True:
            bullet = self.main_class.bullet

            # Vertical alignment with realistic offset
            target_top = bullet.top 
            offset = random.randint(-20, 20)  
            the_new_top = target_top + offset 

            # Gradual vertical movement
            if self.main_class.bot_player.top < the_new_top:
                move_amount = 2  
                self.main_class.bot_player.top += move_amount
            elif self.main_class.bot_player.top > the_new_top:
                move_amount = 2
                self.main_class.bot_player.top -= move_amount

            self.main_class.bot_player.update()
            time.sleep(0.010)
