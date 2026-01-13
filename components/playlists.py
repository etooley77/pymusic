import os

folder = 'music'

playlists = [
	# ['reference name', 'display name', [songs contained]]
	['all_music', 'All Music', [f'{folder}/{f}' for f in os.listdir(folder) if f.split('.')[1] == 'wav']],
    ['playlist', 'Playlist #1', ['music/all_seeing_eye.wav', 'music/ex_nihilo.wav', 'music/galleries_of_morbid_artistry.wav']],
]