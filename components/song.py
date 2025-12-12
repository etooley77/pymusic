import pygame

from constants import WIDTH, WHITE

from helpers import distance

# 
class Song():
    def __init__(self, file):
        self.file = file
        self.loaded = False

        self.is_playing = False
        self.is_paused = False

        # Load files
        # pygame.mixer.music.load(self.file)

        self.play = pygame.image.load("assets/play.png").convert_alpha()
        self.pause = pygame.image.load("assets/pause.png").convert_alpha()

        self.icon = self.play

        # Font
        self.name_font = pygame.font.Font("assets/regular.ttf", 16)

    def setup(self):
        if not self.loaded:
            pygame.mixer.music.load(self.file)
            self.loaded = True

    def play(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(0)
            self.is_playing = True
            self.icon = self.pause

    def pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.icon = self.pause
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.icon = self.play

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.loaded = False
            self.icon = self.play
            self.playing = False
            self.is_paused = False

    def check_click(self, mouse_pos):
        if distance(mouse_pos, self.icon_pos) < 10:
            return True

    # 
    def draw(self, screen, y_pos):
        box = [(WIDTH / 8), y_pos, (6 * WIDTH / 8), 40]
        pygame.draw.rect(screen, WHITE, box, 1, 5, 5, 5, 5)

        self.icon_pos = [box[0] + 20, box[1] + box[3] / 2]
        screen.blit(self.icon, self.icon.get_rect(center = (box[0] + 20, box[1] + box[3] / 2)))

        song_title = self.name_font.render(f"{self.file.split('/')[1]}", True, WHITE)
        screen.blit(song_title, (box[0] + 50, box[1] + box[3] / 2 - song_title.get_height() / 2))