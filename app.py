import pygame
import sys
import shutil

from constants import *
from components.playlists import playlists

from components.button import TextButton
from components.song import Song
# from components.playlist import Playlist

from components.filedialog import open_file_dialog

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

        self.playlists = []
        self.curr_playlist_id = 0
        self.curr_playlist_songs = []

        self.sidebar_offset = 200

        # Font
        self.title_font = pygame.font.Font("assets/bold.ttf", 48)
        self.font = pygame.font.Font("assets/regular.ttf", 24)
        self.font20 = pygame.font.Font("assets/regular.ttf", 20)
        self.font16 = pygame.font.Font("assets/regular.ttf", 16)

        # Current song variables
        self.curr_song = None
        self.curr_song_sound = None
        self.playing = False

        # Song setup
        self.songs = []

        self.setup()
        self.define_playlist()

    # Creates a Song object for every file found. Song objects do not handle the music logic and functionality, but instead only handle things specific to every song, such as what file should be loaded, what should be drawn on screen, and the states that handle UI objects
    def setup(self):
        y_pos = 100

        for song_file in playlists[self.curr_playlist_id][2]:
            obj = Song(song_file, self.play_icon, self.pause_icon)
            self.songs.append(obj)

        for playlist in playlists:
            btn = TextButton(SIDEBAR_WIDTH - 20, 40, f"{playlist[1]}")
            self.playlists.append(btn)

    def layout(self):
        song_y_pos = 100
        playlist_y_pos = 50

        for song in self.curr_playlist_songs:
            song.layout(song_y_pos)
            song_y_pos += 50

        for playlist in self.playlists:
            playlist.layout(10, playlist_y_pos)
            playlist_y_pos += 50

    def define_playlist(self):
        self.curr_playlist_songs = [song for song in self.songs if song.file in playlists[self.curr_playlist_id][2]]

    def setup_selected(self, sel_songs):
        # Add new selected songs below existing ones
        y_pos = 100 + (len(self.songs) * 50)
        dest = "music/"

        for song_file in sel_songs:
            song_file_split = "music/" + song_file.split("/")[-1]
            print(song_file_split)
            print(self.songs)

            # Check if the file already exists
            if not song_file_split in [s.file for s in self.songs]:
                obj = Song(song_file_split, self.play_icon, self.pause_icon)
                self.songs.append(obj)
                if self.curr_playlist_id == 0:
                    self.curr_playlist_songs.append(obj)

                # Define a layout
                obj.layout(y_pos)
                y_pos += 50

                # Move file to music folder
                shutil.copy(song_file, dest)
                # shutil.move(song_file, dest)
            else:
                print("\n\nSong file already exists!\n\n")

    def upload_songs(self):
        selected_file = open_file_dialog()

        if selected_file:
            self.setup_selected([selected_file])

    # 
    # Screens
    # 

    def draw_sidebar(self):
        # The background for the playlist sidebar
        sidebar_rect = pygame.rect.Rect(0, 0, SIDEBAR_WIDTH, HEIGHT)
        pygame.draw.rect(self.screen, DARKEST_GRAY, sidebar_rect)

        # Playlist title text
        playlists_title = self.font20.render("Your playlists", True, WHITE)
        self.screen.blit(playlists_title, (SIDEBAR_WIDTH / 2 - playlists_title.get_width() / 2, 10))

        # Create buttons for each playlist
        for playlist in self.playlists:
            playlist.draw(self.screen)

    def draw_songs(self):
        # Call each song's draw function
        for song in self.curr_playlist_songs:
            song.draw(self.screen)

    def draw_footer(self):
        # Background rect
        footer_rect = pygame.rect.Rect((WIDTH / 4), HEIGHT - 60, WIDTH, 60)
        pygame.draw.rect(self.screen, DARKER_GRAY, footer_rect)

        # Contains the current song file name and a progress bar
        curr_song_title = self.font16.render(f"{self.curr_song.file.split("/")[1]}", True, WHITE)
        self.screen.blit(curr_song_title, (WIDTH / 2 + SIDEBAR_WIDTH / 2 - curr_song_title.get_width() / 2, HEIGHT - curr_song_title.get_height() * 2 - 5))

        # Calculate the progress bar size
        PROGRESS_WIDTH = 3 * WIDTH / 8

        if self.curr_song != None:
            # Get progress and total length of current song
            curr_progress = int(pygame.mixer.music.get_pos() / 1000)
            curr_song_length = int(pygame.mixer.Sound.get_length(self.curr_song_sound))

            if curr_progress % 60 < 10:
                progress_time = f"{int(curr_progress / 60)}:0{curr_progress % 60}"
            else:
                progress_time = f"{int(curr_progress / 60)}:{curr_progress % 60}"

            if curr_song_length % 60 < 10:
                song_time = f"{int(curr_song_length / 60)}:0{curr_song_length % 60}"
            else:
                song_time = f"{int(curr_song_length / 60)}:{curr_song_length % 60}"

            # Put times on screen
            progress_time_label = self.font16.render(progress_time, True, WHITE)
            self.screen.blit(progress_time_label, (WIDTH / 2 + SIDEBAR_WIDTH / 2 - PROGRESS_WIDTH / 2 - progress_time_label.get_width() - 5, HEIGHT - 20 - progress_time_label.get_height() / 2))

            song_time_label = self.font16.render(song_time, True, WHITE)
            self.screen.blit(song_time_label, (WIDTH / 2 + SIDEBAR_WIDTH / 2 + PROGRESS_WIDTH / 2 + 5, HEIGHT - 20 - song_time_label.get_height() / 2))
            
            # Calculate width of progress Rect and the width of the Rect for the rest of the song
            progress_bar_width = (curr_progress / curr_song_length) * PROGRESS_WIDTH
            rest_bar_width = PROGRESS_WIDTH - progress_bar_width

            # Create Rect objects for both bars
            progress_bar = pygame.rect.Rect((WIDTH / 2 + SIDEBAR_WIDTH / 2 - PROGRESS_WIDTH / 2), HEIGHT - 20, progress_bar_width, 3)
            pygame.draw.rect(self.screen, WHITE, progress_bar)

            rest_bar = pygame.rect.Rect(progress_bar.right, HEIGHT - 20, rest_bar_width, 3)
            pygame.draw.rect(self.screen, DARK_GRAY, rest_bar)

    # Home
    def draw_home(self):
        self.draw_sidebar()
        self.draw_songs()
        if self.curr_song != None:
            self.draw_footer()

        your_music_title = self.title_font.render(playlists[self.curr_playlist_id][1], True, WHITE)
        self.screen.blit(your_music_title, (WIDTH / 2 + SIDEBAR_WIDTH / 2 - your_music_title.get_width() / 2, self.curr_playlist_songs[0].rect.y - your_music_title.get_height() - 5))

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
                        if self.curr_song != None:
                            if self.playing: # Song is playing -> pause
                                self.playing = False
                                pygame.mixer.music.pause()
                                self.curr_song.update(self.playing)
                            else: # Song is paused -> unpause
                                self.playing = True
                                pygame.mixer.music.unpause()
                                self.curr_song.update(self.playing)
                    if event.key == pygame.K_u:
                        # Run the upload function
                        self.upload_songs()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        if mouse_pos[0] > SIDEBAR_WIDTH:
                            for song in self.curr_playlist_songs:
                                # Check which song was clicked
                                if song.check_click(mouse_pos):
                                    # If no current song (usually only at start of program)
                                    if self.curr_song == None:
                                        self.curr_song = song # Set current song to correct song
                                        if not self.curr_song.loaded:
                                            # Loads the song to the mixer
                                            pygame.mixer.music.load(self.curr_song.file)
                                            self.curr_song.loaded = True

                                            self.curr_song_sound = pygame.mixer.Sound(self.curr_song.file)

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

                                        self.curr_song_sound = pygame.mixer.Sound(self.curr_song.file)

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
                        else:
                            for button in self.playlists:
                                if button.check_click(mouse_pos):
                                    self.curr_playlist_id = self.playlists.index(button)

                                    # Reload the screen
                                    self.define_playlist()
                                    self.run()

                    elif event.button == 4:
                        # Scroll up
                        top_song = self.curr_playlist_songs[0].rect.y

                        if top_song < 100:
                            for song in self.curr_playlist_songs:
                                song.rect.y += 8
                    # Scroll down
                    elif event.button == 5:
                        bottom_song = self.curr_playlist_songs[-1].rect.y + self.curr_playlist_songs[-1].rect.height

                        if bottom_song > self.screen.get_height() - 75:
                            for song in self.curr_playlist_songs:
                                song.rect.y -= 8


            # Get delta time (time change)
            # dt = self.clock.tick(60)
            
            # Clear screen for next frame
            self.screen.fill(BLACK)

            # Draw screen
            self.draw_home()

            # Update display
            pygame.display.flip()

    # Run function
    def run(self):
        self.layout()
        self.home()