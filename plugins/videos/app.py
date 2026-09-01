"""
date : 31, 08, 2026
autheur : Gnabro Israel
"""
from gateway import ThreadLocker
from logic import AudioHandler
from windows import Window


# the locker
locker = ThreadLocker()

# audio api
audio_api = AudioHandler(locker)


# the  window
window = Window(locker, audio_api,
video_file='/home/gnabro/Bureau/narnia.mkv')


window.start()
