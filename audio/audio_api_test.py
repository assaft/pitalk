from time import sleep

from audio_api_2 import Recorder

reorder = Recorder()

reorder.start_playback("../recordings/PT_2024_12_19-19_52_05_2fbc60ad-7e40-4e25-a364-66d13b124bac.wav")

sleep(5)
reorder.stop_playback()
