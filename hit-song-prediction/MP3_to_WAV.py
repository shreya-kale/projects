# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 00:00:37 2022

@author: HP
"""


import os
import glob
from pydub import AudioSegment

i = 0
all_files = glob.glob('Level_2_Audios_MP3/*.{}'.format('mp3'))

for file in all_files:
    path, ext = os.path.splitext(file)
    name = path.split('\\')
    sound = AudioSegment.from_mp3(file)
    sound.export("Level_2_Audios_WAV/{}.wav".format(name[-1]), format="wav")
    i += 1
    print('Done', i)

print('Done All')
