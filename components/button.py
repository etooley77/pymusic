import pygame

from constants import *

# 
class TextButton():
    def __init__(self, width, height, text):
        self.width = width
        self.height = height

        self.font = pygame.font.Font("assets/regular.ttf", 16)
        self.text = text

        self.rect = None

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def layout(self, x_pos, y_pos):
        rect_values = [x_pos, y_pos, self.width, self.height]
        self.rect = pygame.rect.Rect(rect_values)

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, self.rect, 0, 5, 5, 5, 5)
        else:
            pygame.draw.rect(screen, WHITE, self.rect, 1, 5, 5, 5, 5)

        playlist_title = self.font.render(f"{self.text}", True, WHITE)
        screen.blit(playlist_title, (self.rect.x + 10, self.rect.y + self.rect.height / 2 - playlist_title.get_height() / 2))