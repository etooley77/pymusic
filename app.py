import pygame
import sys

from constants import *
from components.playlists import playlists

from components.button import TextButton
from components.song import Song
# from components.playlist import Playlist

# 
class MusicApp():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Music Listener")
        
        icon = pygame.image.load("assets/icon.ico").convert_alpha()
        pygame.display.set_icon(icon)

        self.play_icon = pygame.image.load("assets/play.png").convert_alpha()
        self.pause_icon = pygame.image.load("assets/pause.png").convert_alpha()

        self.curr_screen = "HOME"
        self.on_screen = True

        # Font
        self.title_font = pygame.font.Font("assets/bold.ttf", 48)
        self.font = pygame.font.Font("assets/regular.ttf", 24)
        self.font16 = pygame.font.Font("assets/regular.ttf", 16)

        # Music variables
        self.curr_song = None
        self.playing = False

        self.songs = []

        self.setup()

    def setup(self):
        for song_file in playlists[0][2]:
            obj = Song(song_file)
            self.songs.append(obj)

        print(self.songs)

    # 
    # Screens
    # 

    def draw_navbar(self):
        nav_title = self.font.render("App", True, WHITE)
        self.screen.blit(nav_title, (WIDTH / 8 - nav_title.get_width() / 2, 5))

    def draw_songs(self, start_pos):
        pos = start_pos
        for song in self.songs:
            song.draw(self.screen, pos)
            pos += 50

    # Home
    def draw_home(self):
        all_playlists = self.title_font.render("Your Playlists", True, WHITE)
        self.screen.blit(all_playlists, (WIDTH / 2 - all_playlists.get_width() / 2, all_playlists.get_height() + 5))

        self.draw_songs(150)

    def home(self):
        self.on_screen = True
        while self.on_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.curr_song = self.songs[0]
                        self.curr_song.setup()
                        self.curr_song.play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for song in self.songs:
                        # Check which song was clicked
                        if song.check_click(mouse_pos):
                            # If no current song
                            if self.curr_song == None:
                                self.curr_song = song
                                self.curr_song.setup()
                                self.curr_song.play()
                            # If the selected song is different than the current song
                            elif song != self.curr_song:
                                self.curr_song.stop()
                                self.curr_song = song
                                self.curr_song.setup()
                                self.curr_song.play()
                            else:
                                self.curr_song.pause()

            # Get delta time
            dt = self.clock.tick(60)
            
            # Clear screen for next frame
            self.screen.fill(BLACK)

            # Draw screen
            self.draw_navbar()
            self.draw_home()

            # Update display
            pygame.display.flip()

    # Run function
    def run(self):
        match self.curr_screen:
            case "HOME":
                self.home()