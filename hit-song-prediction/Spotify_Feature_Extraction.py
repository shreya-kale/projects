# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:12:43 2021

@author: HP
"""


# Importing All Required Modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


# Establishing Connection with the Spotify API
ClientId = '171c5dc3ef654d4eadacda6cef9bda14'
SecretKey = 'e81313056fcf49b5a84eb96ecbbb21f1'
auth_manager= SpotifyClientCredentials(client_id=ClientId, client_secret=SecretKey)
sp = spotipy.Spotify(auth_manager=auth_manager)


# Firing the Search Query to Spotify API
search = sp.search(q='genre:"indian"', type='track', limit=50, offset=950, market='IN')

'''
# Creating CSV File for Search Query Results
searchDF = pd.DataFrame(search)
searchDF = searchDF.T
searchDF.to_csv("L1_Search_Query_Results.csv")
'''
'''
# Creating CSV File for 'tracks' Column of searchDF
tracksDF = pd.DataFrame(search['tracks'])
tracksDF.to_csv("L2_Tracks_Results.csv")
'''

# Creating CSV File for 'items' Column of tracksDF
itemsDF = pd.DataFrame(search['tracks']['items'])
itemsDF.to_csv("Improved/Demo_Review.csv")

# Creating CSV File for 'audio_features_extracted' for each ID:
feature_dict = {}
for name in itemsDF['id']:
    feature_dict[name] = sp.audio_features(name)
new_dict={}
for k, v in feature_dict.items():
    new_dict[k] = v[0]
    
df3 = pd.DataFrame(new_dict)
dictT = df3.T
dictT.to_csv("Improved/Extracted_Features_1000.csv")

print('Done')