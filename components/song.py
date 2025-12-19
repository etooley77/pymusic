import pygame

from constants import WIDTH, WHITE, DARK_GRAY

# 
class Song():
    def __init__(self, file, play_button, pause_button):
        self.file = file
        self.loaded = False

        self.play_icon = play_button
        self.pause_icon = pause_button

        self.icon = self.play_icon

        # Font
        self.name_font = pygame.font.Font("assets/regular.ttf", 16)

        # Handle the layout
        self.rect = None
        self.icon_pos = None

    def update(self, playing):
        if playing:
            self.icon = self.pause_icon
        else:
            self.icon = self.play_icon

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    # 
    def layout(self, y_pos):
        rect_values = [(WIDTH / 8), y_pos, (6 * WIDTH / 8), 40]
        self.rect = pygame.rect.Rect(rect_values)

        self.icon_pos = [self.rect.x + 20, self.rect.y + self.rect.width / 2]

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, self.rect, 0, 5, 5, 5, 5)
        else:
            pygame.draw.rect(screen, WHITE, self.rect, 1, 5, 5, 5, 5)

        screen.blit(self.icon, self.icon.get_rect(center = (self.rect.x + 20, self.rect.y + self.rect.height / 2)))

        song_title = self.name_font.render(f"{self.file.split('/')[1]}", True, WHITE)
        screen.blit(song_title, (self.rect.x + 50, self.rect.y + self.rect.height / 2 - song_title.get_height() / 2))