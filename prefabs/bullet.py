import flet, time, random




class Bullet (flet.Container):
    def __init__ (self, main_class, limit_of_left:int):
        super().__init__()
        self.main_class = main_class
        self.limit_of_left = limit_of_left

        self.bgcolor = "white"
        self.width = 50
        self.height = 50

        self.direction = "left"
        self.break_per_step = 0

        self.speed = 10
    

    def step (self):
        if self.direction == "left":
            self.left = self.left - self.speed
        else:
            self.left = self.left + self.speed

        self.top = self.top + self.break_per_step
        self.update()
    

    def movement_effector(self):
        # Do not pass window borders
        if self.top < 0:
            self.break_per_step = 5
        elif self.top > self.main_class.page.height:
            self.break_per_step = -5
        
        if self.left < 0:
            self.direction = "right"
            #? Play negative sound when the player misses the bullet
            self.main_class.audio_manager.negative_sound.play() # Plays sound
            self.main_class.reply_emoji_effect(random.choice(["😵", "😕", "🤬", "😐", "😵‍💫"])) # Show an emoji effect
            self.main_class.punish("player")
        elif self.left > self.main_class.page.width:
            self.direction = "left"
            self.main_class.punish("bot")


        around_player_top = range(self.main_class.player_paddle.top - 15, self.main_class.player_paddle.top + 150 + 15)
        around_bot_top = range(self.main_class.bot_player.top - 15, self.main_class.bot_player.top + 150 + 15)


        if self.left < 50 and self.top in around_player_top:
            self.direction = "right"
            break_top_up_range = range(self.main_class.player_paddle.top - 15, self.main_class.player_paddle.top + 15)
            break_top_down_range = range(self.main_class.player_paddle.top + 150 - 15, self.main_class.player_paddle.top + 150 + 15)

            if self.top in break_top_up_range:
                self.break_per_step = -5
            elif self.top in break_top_down_range:
                self.break_per_step = 5
            
            # Add the score for the player in the scores label
            self.main_class.player_score_text.value = str(int(self.main_class.player_score_text.value)+1)
            self.main_class.player_score_text.update()

            # Play the positive sound when the player hit the bullet
            self.main_class.audio_manager.positive_sound.play()
        elif self.left > self.limit_of_left-100 and self.top in around_bot_top:
            self.direction = "left"
            break_top_up_range = range(self.main_class.bot_player.top - 15, self.main_class.bot_player.top + 15)
            break_top_down_range = range(self.main_class.bot_player.top + 150 - 15, self.main_class.bot_player.top + 150 + 15)

            if self.top in break_top_up_range:
                self.break_per_step = -5
            elif self.top in break_top_down_range:
                self.break_per_step = 5
            
            # Add the score for the bot in the scores label
            self.main_class.bot_score_text.value = str(int(self.main_class.bot_score_text.value)+1)
            self.main_class.bot_score_text.update()


    def move (self):
        times_of_repeat = 0
        while True:
            self.step()
            self.movement_effector()
            time.sleep(0.025)
            times_of_repeat = times_of_repeat + 1
            if times_of_repeat == 250:
                self.speed = self.speed + 2.5
                times_of_repeat = 0