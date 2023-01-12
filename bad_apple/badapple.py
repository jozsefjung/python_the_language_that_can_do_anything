import pygame as pg


class Frame:
    def __init__(self, fn, image, rect):
        self.frame_number = fn
        self.image = image
        self.rect = rect
        if (
            self.rect.width != self.image.get_width()
            or self.rect.height != self.image.get_height()
        ):
            self.image = pg.transform.smoothscale(
                self.image, (self.rect.width, self.rect.height)
            )

    def draw(self, surface: pg.Surface):
        surface.blit(self.image, self.rect)


class Animation:
    def __init__(self, frame_name_pattern: str, number_of_frames: int, music: str):
        self.frame_name_pattern = frame_name_pattern
        self.number_of_frames = number_of_frames
        self.frames = self.load_frames()
        pg.mixer.music.load(music)
        self.current_frame = next(self.frames)
        self.frame_font = pg.font.SysFont(None, 36)  # noqa
        self.end_font = pg.font.SysFont(None, 144)  # noqa
        self.end = False

    def draw(self, screen):
        if self.end:
            pg.mixer.music.stop()
            img = self.end_font.render("Pitanja?", True, pg.Color("white"))
            screen.blit(img, (480 - img.get_width() // 2, 360 - img.get_height() // 2))
            return

        try:
            if not pg.mixer.music.get_busy():
                pg.mixer.music.play()
            self.current_frame.draw(screen)
            screen.blit(
                self.frame_font.render(
                    f"Frame {self.current_frame.frame_number}", True, pg.Color("red")
                ),
                (10, 10),
            )
            self.current_frame = next(self.frames)
        except StopIteration:
            pg.mixer.music.stop()
            self.end = True

    def load_frames(self):
        for i in range(self.number_of_frames):
            yield Frame(
                i,
                pg.image.load(self.frame_name_pattern.format(i)),
                pg.Rect(0, 0, 960, 720),
            )


def main():
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((960, 720), flags=pg.HWSURFACE | pg.DOUBLEBUF, vsync=1)
    pg.display.set_caption("Bad Python")
    pg.display.set_icon(pg.image.load("assets/frame253.png"))

    running = True
    clock = pg.time.Clock()

    animation = Animation("assets/frame{}.png", 6571, "assets/music.mp3")
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(pg.Color("black"))
        animation.draw(screen)
        pg.display.flip()
        clock.tick(31)


if __name__ == "__main__":
    main()
