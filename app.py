import pygame
import sys

from constants import *

# 
class MusicApp():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Music Listener")
        
        icon = pygame.image.load("assets/icon.ico").convert_alpha()
        pygame.display.set_icon(icon)

        self.curr_screen = "HOME"
        self.on_screen = True

        # Font
        self.title_font = pygame.font.Font("assets/bold.ttf", 48)
        self.font = pygame.font.Font("assets/regular.ttf", 24)

        # Music variables
        self.curr_song = None
        self.playing = False

    # Screens
    def home(self):
        self.on_screen = True
        while self.on_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Get delta time
            dt = self.clock.tick(60)
            
            # Clear screen for next frame
            self.screen.fill(BLACK)

            # Update display
            pygame.display.flip()

    # Run function
    def run(self):
        match self.curr_screen:
            case "HOME":
                self.home()