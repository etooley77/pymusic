import os

folder = 'music'

playlists = [
	# ['reference name', 'display name', [songs contained]]
	['all_music', 'All Music', [f'{folder}/{f}' for f in os.listdir(folder) if f.split('.')[1] == 'wav']]
]