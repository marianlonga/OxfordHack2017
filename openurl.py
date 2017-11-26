import webbrowser
from random import randint

def play_cat_video():
	with open('cat_videos.txt') as f:
		cat_videos = f.readlines()
	cat_videos = [cat_video.strip() for cat_video in cat_videos]

	random_cat_video = cat_videos[randint(0, len(cat_videos)-1)]

	url = random_cat_video + "?t=10s"

	# MacOS
	chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

	# Windows
	# chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

	# Linux
	# chrome_path = '/usr/bin/google-chrome %s'

	webbrowser.get(chrome_path).open(url)