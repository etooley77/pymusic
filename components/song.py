import pygame

from constants import WIDTH, WHITE

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

    def play_pause(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.icon = self.pause
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.icon = self.play
        else:
            pygame.mixer.music.play(0)
            self.is_playing = True
            self.icon = self.pause

    # 
    def draw(self, screen, y_pos):
        box = [(WIDTH / 8), y_pos, (6 * WIDTH / 8), 40]
        pygame.draw.rect(screen, WHITE, box, 1, 5, 5, 5, 5)

        screen.blit(self.icon, self.icon.get_rect(center = (box[0] + 20, box[1] + box[3] / 2)))

        song_title = self.name_font.render(f"{self.file.split('/')[1]}", True, WHITE)
        screen.blit(song_title, (box[0] + 50, box[1] + box[3] / 2 - song_title.get_height() / 2))