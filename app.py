import pygame
import sys
import shutil, os
from random import shuffle

from constants import *
from components.playlists import playlists

from components.button import *
from components.song import Song
# from components.playlist import Playlist

from components.filedialog import open_file_dialog

from helpers import check_file_name_length

# App class
class MusicApp():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()

        # Screen setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Music Listener")
        
        # Icons
        icon = pygame.image.load("assets/icon.ico").convert_alpha()
        pygame.display.set_icon(icon)
        self.play_icon = pygame.image.load("assets/play.png").convert_alpha()
        self.pause_icon = pygame.image.load("assets/pause.png").convert_alpha()

        # Buttons
        self.upload_btn = None

        # Playlist song handling
        self.playlists = []
        self.curr_playlist_id = 0

        # Handle shuffling
        self.curr_playlist_shuffle = None

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
        self.curr_playlist_songs = []

        self.setup()
        self.define_playlist()

    # Creates a Song object for every file found. Song objects do not handle the music logic and functionality, but instead only handle things specific to every song, such as what file should be loaded, what should be drawn on screen, and the states that handle UI objects
    def setup(self):
        # Create song objects for all the songs found in the "All Music" playlist
        for song_file in playlists[self.curr_playlist_id][2]:
            obj = Song(song_file, self.play_icon, self.pause_icon)
            self.songs.append(obj)

        # Create button objects for each playlist
        for playlist in playlists:
            btn = TextButtonBorder(SIDEBAR_WIDTH - SIDEBAR_WIDTH / 10, 40, f"{playlist[1]}")
            self.playlists.append(btn)

        # Create upload button object
        self.upload_btn = TextButton(SIDEBAR_WIDTH - SIDEBAR_WIDTH / 10, 40, "Upload more")

    def layout(self):
        # Starting y positions for the songs and playlist buttons
        song_y_pos = 100
        playlist_y_pos = 50

        # Call the layout function for each song
        for song in self.curr_playlist_songs:
            song.layout(song_y_pos)
            song_y_pos += 50

        # Call the layout function for each playlist button
        for playlist in self.playlists:
            playlist.layout(10, playlist_y_pos)
            playlist_y_pos += 50

        # Functional buttons
        # Layout the upload button
        self.upload_btn.layout(SIDEBAR_WIDTH / 20, HEIGHT - (self.upload_btn.height + 10))

    def define_playlist(self):
        # Add the song files from the selected playlist into `self.curr_playlist_songs`
        self.curr_playlist_songs = [song for song in self.songs if song.file in playlists[self.curr_playlist_id][2]]

    def setup_selected(self, sel_songs):
        # Add new selected songs below existing ones
        y_pos = self.curr_playlist_songs[-1].rect.bottom + 10
        dest = "music/"

        for song_file in sel_songs:
            # Shorten the path to the song file
            song_file_split = "music/" + check_file_name_length(song_file)

            # Check if the file already exists
            if not song_file_split in [s.file for s in self.songs]:
                # Temporarily add the song manually to the playlist "All Music". Next time the program runs, it is added automatically because it is in the `music` folder.
                playlists[0][2].append(song_file_split)

                # Create an object for each song and add it to `self.songs`. If the user is currently viewing the "All Music", then add the song object to `self.curr_playlist_songs` as well.
                obj = Song(song_file_split, self.play_icon, self.pause_icon)
                self.songs.append(obj)
                if self.curr_playlist_id == 0:
                    self.curr_playlist_songs.append(obj)

                # Call the layout function of the song
                obj.layout(y_pos)
                y_pos += 50

                # Move/copy file to music folder
                shutil.copy(song_file, dest)
                # shutil.move(song_file, dest)
            else:
                print("\n\nSong file already exists!\n\n")

    def upload_songs(self):
        # Call the function to open the tkinter file dialog (from `components/filedialog.py`)
        selected_file = open_file_dialog()

        # If a file was selected and opened
        if selected_file:
            self.setup_selected([selected_file])

    def shuffle_play(self):
        # Update the old song
        pygame.mixer.music.stop()
        self.playing = False

        if self.curr_song is not None:
            self.curr_song.update(self.playing)

        self.curr_song = self.curr_playlist_shuffle[0]
        if not self.curr_song.loaded:
            # Loads the song to the mixer
            pygame.mixer.music.load(self.curr_song.file)
            self.curr_song.loaded = True

            self.curr_song_sound = pygame.mixer.Sound(self.curr_song.file)

        # Play the song and update program states, which updates the UI
        pygame.mixer.music.play()
        self.playing = True
        self.curr_song.update(self.playing)

    # 
    # Screens
    # 

    # Components
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

        # Draw the upload button
        self.upload_btn.draw(self.screen)

    def draw_songs(self):
        # Call each song's draw function
        for song in self.curr_playlist_songs:
            song.draw(self.screen)

    def draw_footer(self):
        # Background of the footer rect
        footer_rect = pygame.rect.Rect((WIDTH / 4), HEIGHT - 60, WIDTH, 60)
        pygame.draw.rect(self.screen, DARKER_GRAY, footer_rect)

        # The current song file that is playing
        curr_song_title = self.font16.render(f"{self.curr_song.file.split("/")[1]}", True, WHITE)
        self.screen.blit(curr_song_title, (WIDTH / 2 + SIDEBAR_WIDTH / 2 - curr_song_title.get_width() / 2, HEIGHT - curr_song_title.get_height() * 2 - 5))

        # Calculate the progress bar size
        PROGRESS_WIDTH = 3 * WIDTH / 8

        # Only display the progress bar if there is a song playing
        if self.curr_song != None:
            # Get progress and total length of current song
            curr_progress = int(pygame.mixer.music.get_pos() / 1000)
            curr_song_length = int(pygame.mixer.Sound.get_length(self.curr_song_sound))

            # Check the state of the currently playing song
            if curr_progress >= curr_song_length and self.curr_playlist_shuffle is not None:
                # Remove the song that just ended
                self.curr_playlist_shuffle.remove(self.curr_song)

                # Play the next song in the shuffle
                self.shuffle_play()

            # Display the amount of time that has passed
            if curr_progress % 60 < 10:
                progress_time = f"{int(curr_progress / 60)}:0{curr_progress % 60}"
            else:
                progress_time = f"{int(curr_progress / 60)}:{curr_progress % 60}"

            # Get the total song length
            if curr_song_length % 60 < 10:
                song_time = f"{int(curr_song_length / 60)}:0{curr_song_length % 60}"
            else:
                song_time = f"{int(curr_song_length / 60)}:{curr_song_length % 60}"

            # Display the times on either side of the progress bar
            progress_time_label = self.font16.render(progress_time, True, WHITE)
            self.screen.blit(progress_time_label, (WIDTH / 2 + SIDEBAR_WIDTH / 2 - PROGRESS_WIDTH / 2 - progress_time_label.get_width() - 5, HEIGHT - 20 - progress_time_label.get_height() / 2))

            song_time_label = self.font16.render(song_time, True, WHITE)
            self.screen.blit(song_time_label, (WIDTH / 2 + SIDEBAR_WIDTH / 2 + PROGRESS_WIDTH / 2 + 5, HEIGHT - 20 - song_time_label.get_height() / 2))
            
            # Calculate width of progress Rect and the width of the Rect for the rest of the song
            progress_bar_width = (curr_progress / curr_song_length) * PROGRESS_WIDTH
            rest_bar_width = PROGRESS_WIDTH - progress_bar_width

            # Create and draw Rect objects for both bars
            progress_bar = pygame.rect.Rect((WIDTH / 2 + SIDEBAR_WIDTH / 2 - PROGRESS_WIDTH / 2), HEIGHT - 20, progress_bar_width, 3)
            pygame.draw.rect(self.screen, WHITE, progress_bar)

            rest_bar = pygame.rect.Rect(progress_bar.right, HEIGHT - 20, rest_bar_width, 3)
            pygame.draw.rect(self.screen, DARK_GRAY, rest_bar)

    # Home screen
    def draw_home(self):
        # Call draw functions to draw screen elements
        self.draw_sidebar()
        self.draw_songs()
        if self.curr_song != None:
            self.draw_footer()

        # Render either "All Music" or the name of the playlist
        your_music_title = self.title_font.render(playlists[self.curr_playlist_id][1], True, WHITE)
        self.screen.blit(your_music_title, (WIDTH / 2 + SIDEBAR_WIDTH / 2 - your_music_title.get_width() / 2, self.curr_playlist_songs[0].rect.y - your_music_title.get_height() - 5))

    def home(self):
        self.on_screen = True
        while self.on_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Keydown events
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
                    if event.key == pygame.K_s:
                        # Reshuffle the current playlist and start playing
                        if self.curr_playlist_shuffle is not None:
                            shuffle(self.curr_playlist_shuffle)
                            self.shuffle_play()
                        else:
                            self.curr_playlist_shuffle = [song for song in self.curr_playlist_songs]
                            shuffle(self.curr_playlist_shuffle)
                            self.shuffle_play()
                # Mouse button events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()

                        # If the user clicks in the song panel
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

                                        # Shuffle the current playlist songs, without the current song
                                        self.curr_playlist_shuffle = shuffle([song for song in self.curr_playlist_songs if song != self.curr_song])

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
                        # If the user clicks on the sidebar
                        else:
                            # Check if the user clicks on one of the playlists
                            for button in self.playlists:
                                if button.check_click(mouse_pos):
                                    self.curr_playlist_id = self.playlists.index(button)

                                    # Reload the screen
                                    self.define_playlist()
                                    self.run()

                            # Check if the upload button was clicked
                            if self.upload_btn.check_click(mouse_pos):
                                self.upload_songs()

                    # Scroll up event
                    elif event.button == 4:
                        top_song = self.curr_playlist_songs[0].rect.y

                        if top_song < 100:
                            for song in self.curr_playlist_songs:
                                song.rect.y += 8
                    # Scroll down event
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