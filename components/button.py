import pygame

from constants import *

btn_font = "assets/regular.ttf"

# 
class TextButtonBorder():
    def __init__(self, width, height, text):
        self.width = width
        self.height = height

        self.font = pygame.font.Font(btn_font, 16)
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

        button_title = self.font.render(f"{self.text}", True, WHITE)
        screen.blit(button_title, (self.rect.x + 10, self.rect.y + self.rect.height / 2 - button_title.get_height() / 2))

class TextButton():
    def __init__(self, width, height, text):
        self.width = width
        self.height = height

        self.font = pygame.font.Font(btn_font, 16)
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
        button_title = self.font.render(f"{self.text}", True, WHITE)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARKEST_GRAY, self.rect, 0, 5, 5, 5, 5)
            pygame.draw.line(screen, WHITE, (self.rect.x, self.rect.centery + button_title.get_height() / 2 + 3), (self.rect.x + self.width, self.rect.centery + button_title.get_height() / 2 + 3), 1)
        else:
            pygame.draw.rect(screen, DARKEST_GRAY, self.rect, 0, 5, 5, 5, 5)

        
        screen.blit(button_title, (self.rect.centerx - button_title.get_width() / 2, self.rect.y + self.rect.height / 2 - button_title.get_height() / 2))