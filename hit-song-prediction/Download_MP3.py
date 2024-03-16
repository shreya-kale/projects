# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:44:35 2022

@author: HP
"""


import os
import pandas as pd

file = pd.read_csv('Improved/Level_2 - Complete_Data.csv',squeeze=True).to_dict()

ids = list(file['id'].values())

for id in ids:
    query = 'spotdl https://open.spotify.com/track/' + id
    chk = os.system(query)
    if chk == 0:
        print(id)

print('Done')
