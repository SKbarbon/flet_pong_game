from prefabs.paddle import Paddle
from prefabs.bullet import Bullet
from utils.bot_system import BotMovementSystem
from utils.audio_manager import AudioManager
import flet, time, threading


class Pong:
    def __init__(self, page: flet.Page) -> None:
        self.page = page

        page.spacing = 0
        page.padding = 0
        page.bgcolor = "black"
        page.window_full_screen = True
        page.fonts = {
            "Minecraft": "/fonts/Minecraft.ttf"
        }
        page.update()
        time.sleep(0.5)
        page.window_resizable = False
        page.update()
        time.sleep(1)
        # page.window_center()

        # events
        page.on_keyboard_event = self.keyboard_event

        # Sound and music
        self.audio_manager = AudioManager()
        self.audio_manager.setup_all(page=page)


        self.main_stack = flet.Stack()
        page.add(self.main_stack)

        # Player Paddle
        self.player_paddle = Paddle()
        self.main_stack.controls.append(self.player_paddle)
        self.main_stack.update()
        self.player_paddle.top = 50


        # bot player
        self.bot_player = Paddle()
        self.main_stack.controls.append(self.bot_player)
        self.main_stack.update()
        self.bot_player.top = 400
        self.bot_player.right = 0


        # Bullet
        self.bullet = Bullet(main_class=self, limit_of_left=page.width)
        self.main_stack.controls.append(self.bullet)
        self.main_stack.update()
        self.bullet.top = page.height / 2 - (self.bullet.height)
        self.bullet.left = page.width / 2 - (self.bullet.width)

        page.update()


        # Labels
        self.player_score_text = flet.Text("1", color="white", size=200, font_family="Minecraft")
        self.bot_score_text = flet.Text("1", color="white", size=200, font_family="Minecraft")
        self.scores_row = flet.Row([self.player_score_text, flet.Text(":", color="white", size=200, font_family="Minecraft"), self.bot_score_text],
                                width=page.width, alignment=flet.MainAxisAlignment.CENTER)
        self.main_stack.controls.append(self.scores_row)
        self.scores_row.top = 150
        self.scores_row.left = self.page.width / 2 - self.scores_row.width / 2
        self.main_stack.update()

        # Emoji Effect label
        self.emoji_effect_label_text = flet.Text("", width=250, height=250, text_align=flet.TextAlign.CENTER, size=150)
        self.emoji_effect_label_row = flet.Row([self.emoji_effect_label_text],
                                               alignment=flet.MainAxisAlignment.CENTER,
                                               top=page.height / 2 - self.emoji_effect_label_text.width / 2,
                                               left=page.width / 2 - self.emoji_effect_label_text.height / 2,
                                               width=250, height=250
                                               )
        self.main_stack.controls.append(self.emoji_effect_label_row)
        self.main_stack.update()

        # Start bullet move
        threading.Thread(target=self.bullet.move, daemon=True).start()

        # Start bot player move
        BMS = BotMovementSystem(main_class=self)
        threading.Thread(target=BMS.movement, daemon=True).start()
    

    def keyboard_event (self, e):
        if str(e.key).lower() == "arrow down":
            self.player_paddle.move_down()
        elif str(e.key).lower() == "arrow up":
            self.player_paddle.move_up()
    

    def punish (self, which_player):
        if which_player == "player":
            self.player_score_text.value = str(int(self.player_score_text.value)-1)
            self.player_score_text.update()
            if int(self.player_score_text.value) <= 0:
                self.audio_manager.lose_sound.play()
                self.reply_emoji_effect("☠️")
                self.stop_game("You lose")
        elif which_player == "bot":
            self.bot_score_text.value = str(int(self.bot_score_text.value)-1)
            self.bot_score_text.update()
            if int(self.bot_score_text.value) <= 0:
                self.audio_manager.win_sound.play()
                self.reply_emoji_effect("😇")
                self.stop_game("You win!")
        
    
    def reply_emoji_effect(self, emoji): threading.Thread(target=self.__reply_emoji_effect, args=[emoji], daemon=True).start()
    def __reply_emoji_effect (self, emoji):
        self.emoji_effect_label_text.value = emoji
        self.emoji_effect_label_text.visible = True
        self.emoji_effect_label_text.size = 150
        self.emoji_effect_label_text.update()

        for i in range(7):
            time.sleep(0.2)
            if self.emoji_effect_label_text.visible == True:
                self.emoji_effect_label_text.visible = False
            else:
                self.emoji_effect_label_text.visible = True
            self.emoji_effect_label_text.update()
    

    def stop_game (self, done_Text=""):
        self.emoji_effect_label_text2 = flet.Text(done_Text, height=250, text_align=flet.TextAlign.CENTER, size=40, 
                                                  font_family="Minecraft")
        self.emoji_effect_label_row2 = flet.Row([self.emoji_effect_label_text2],
                                               alignment=flet.MainAxisAlignment.CENTER,
                                               top=self.page.height / 2 + 80,
                                               left=0,
                                               width=self.page.width, height=250
                                               )
        self.main_stack.controls.append(self.emoji_effect_label_row2)
        self.main_stack.update()

        self.freeze_game()


    def freeze_game (self):
        while True:
            pass




flet.app(target=Pong, assets_dir="assets")