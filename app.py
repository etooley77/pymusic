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

        self.scroll_offset = 0

        # Font
        self.title_font = pygame.font.Font("assets/bold.ttf", 48)
        self.font = pygame.font.Font("assets/regular.ttf", 24)
        self.font16 = pygame.font.Font("assets/regular.ttf", 16)

        # Current song variables
        self.curr_song = None
        self.playing = False

        # Song setup
        self.songs = []

        self.setup()

    # Creates a Song object for every file found. Song object do not handle the music logic and functionality, but instead only handle things specific to every song, such as what file should be loaded, what should be drawn on screen, and the states that handle UI objects
    def setup(self):
        y_pos = 150 - self.scroll_offset

        for song_file in playlists[0][2]:
            obj = Song(song_file, self.play_icon, self.pause_icon)
            self.songs.append(obj)

            # Define a layout for the current song, and define the starting position for the next song, so no overlapping occurs
            obj.layout(y_pos)
            y_pos += 50

    # 
    # Screens
    # 

    def draw_navbar(self):
        nav_title = self.font.render("Music App", True, WHITE)
        self.screen.blit(nav_title, (WIDTH / 8 - nav_title.get_width() / 2, 5))

    def draw_songs(self):
        for song in self.songs:
            song.draw(self.screen)

    # Home
    def draw_home(self):
        all_playlists = self.title_font.render("Your Music", True, WHITE)
        self.screen.blit(all_playlists, (WIDTH / 2 - all_playlists.get_width() / 2, all_playlists.get_height() + 5))

        self.draw_songs()

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
                        pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for song in self.songs:
                        # Check which song was clicked
                        if song.check_click(mouse_pos):
                            # If no current song (usually only at start of program)
                            if self.curr_song == None:
                                self.curr_song = song # Set current song to correct song
                                if not self.curr_song.loaded:
                                    # Loads the song to the mixer
                                    pygame.mixer.music.load(self.curr_song.file)
                                    self.curr_song.loaded = True

                                # Play the song and update program states, which updates the UI
                                pygame.mixer.music.play()
                                self.playing = True
                                self.curr_song.update(self.playing)

                            # If the selected song is different than the current song
                            elif song != self.curr_song:
                                # Stop old song and setup new song, which updates the UI
                                pygame.mixer.music.stop()
                                self.playing = False
                                self.curr_song.update(self.playing)

                                # Load the new song onto the mixer and update song state `loaded`
                                self.curr_song = song
                                pygame.mixer.music.load(self.curr_song.file)
                                self.curr_song.loaded = True

                                # Play new song and update program states, which updates the UI
                                pygame.mixer.music.play()
                                self.playing = True
                                self.curr_song.update(self.playing)

                            # If the user clicks on the same song (pause/unpause functionality)
                            else:
                                # Make sure that the user cannot pause or unpause songs before a song has even been played
                                if self.curr_song != None:
                                    if self.playing: # Song is playing -> pause
                                        self.playing = False
                                        pygame.mixer.music.pause()
                                        self.curr_song.update(self.playing)
                                    else: # Song is paused -> unpause
                                        self.playing = True
                                        pygame.mixer.music.unpause()
                                        self.curr_song.update(self.playing)



            # Get delta time
            # dt = self.clock.tick(60)
            
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