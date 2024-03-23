import flet



class AudioManager:
    def __init__(self) -> None:
        self.background_music = flet.Audio(
            src="/music/8Bit Arcade Mode.mp3",
            autoplay=True,
            release_mode="loop",
            volume=0.1
        )

        self.positive_sound = flet.Audio(
            src="/sounds/8-Bit (1).mp3"
        )

        self.negative_sound = flet.Audio(
            src="/sounds/8-Bit Fireball Hit.mp3"
        )

        self.lose_sound = flet.Audio(
            src="/sounds/8-Bit.mp3"
        )

        self.win_sound = flet.Audio(
            src="/sounds/8-Bit Sound 6993.mp3"
        )
    

    def setup_all (self, page: flet.Page):
        page.overlay.append(self.background_music)
        page.overlay.append(self.positive_sound)
        page.overlay.append(self.negative_sound)
        page.overlay.append(self.lose_sound)
        page.overlay.append(self.win_sound)

        page.update()