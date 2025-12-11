from pygame import mixer

# 
class Song():
    def __init__(self, file):
        self.file = file

        self.is_playing = False
        self.is_paused = False

        mixer.music.load(file)
    
    def play_pause(self):
        if self.is_playing:
            if self.is_paused:
                mixer.music.unpause()
                self.is_paused = False
            else:
                mixer.music.pause()
                self.is_paused = True
        else:
            mixer.music.play(0)
            self.is_playing = True

    # 
    def draw():
        return