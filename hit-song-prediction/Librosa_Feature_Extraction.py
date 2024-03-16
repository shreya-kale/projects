# -*- coding: utf-8 -*-
"""
Created on Wed May 11 21:35:03 2022

@author: HP
"""

import librosa
import librosa.display
import IPython
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob

#uploading song for processing
from glob import glob

norm_data_dir = './'

audio = glob(norm_data_dir + '*.mp3')

#creating empty csv file(all value ionitialize to 0.0)
header =['Song','chroma_mean_0','chroma_mean_1','chroma_mean_2','chroma_mean_3','chroma_mean_4','chroma_mean_5','chroma_mean_6','chroma_mean_7','chroma_mean_8','chroma_mean_9','chroma_mean_10','chroma_mean_11','chroma_std_0','chroma_std_1','chroma_std_2','chroma_std_3','chroma_std_4','chroma_std_5','chroma_std_6','chroma_std_7','chroma_std_8','chroma_std_9','chroma_std_10','chroma_std_11','mfccs_mean_0','mfccs_mean_1','mfccs_mean_2','mfccs_mean_3','mfccs_mean_4','mfccs_mean_5','mfccs_mean_6','mfccs_mean_7','mfccs_mean_8','mfccs_mean_9','mfccs_mean_10','mfccs_mean_11','mfccs_mean_12','mfccs_std_0','mfccs_std_1','mfccs_std_2','mfccs_std_3','mfccs_std_4','mfccs_std_5','mfccs_std_6','mfccs_std_7','mfccs_std_8','mfccs_std_9','mfccs_std_10','mfccs_std_11','mfccs_std_12','cent_mean','cent_std','cent_skew','contrast_mean_0','contrast_mean_1','contrast_mean_2','contrast_mean_3','contrast_mean_4','contrast_mean_5','contrast_mean_6','contrast_std_0','contrast_std_1','contrast_std_2','contrast_std_3','contrast_std_4','contrast_std_5','contrast_std_6','rolloff_mean','rolloff_std','rolloff_skew','zrate_mean','zrate_std','zrate_skew','tempo']
final_df = pd.DataFrame(columns=header)

for i in range(0,100):#range can be changed according to nummber of songs this is for 100 songs
  final_df.loc[i]=0.0

Y = []
Sr = []
for j in range(0,26):
  file = audio[j]
  tempy , tempsr = librosa.load(file,sr=None)
  #Y.append(tempy)
  #Sr.append(tempsr)
  final_df['Song'].loc[j] = audio[j]
  #y=Y[j]
  #sr=Sr[j]
  y=tempy
  sr=tempsr
  y_harmonic, y_percussive = librosa.effects.hpss(y)
  tempo, beat_frames = librosa.beat.beat_track(y=y_harmonic, sr=sr)
  chroma=librosa.feature.chroma_cens(y=y_harmonic, sr=sr)
  mfccs = librosa.feature.mfcc(y=y_harmonic, sr=sr, n_mfcc=13)
  cent = librosa.feature.spectral_centroid(y=y, sr=sr)
  contrast=librosa.feature.spectral_contrast(y=y_harmonic,sr=sr)
  rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
  zrate=librosa.feature.zero_crossing_rate(y_harmonic)

  chroma_mean=np.mean(chroma,axis=1)
  chroma_std=np.std(chroma,axis=1)

  for i in range(0,12):
      final_df['chroma_mean_'+str(i)].loc[j]=chroma_mean[i]
  for i in range(0,12):
      final_df['chroma_std_'+str(i)].loc[j]=chroma_std[i]

  mfccs_mean=np.mean(mfccs,axis=1)
  mfccs_std=np.std(mfccs,axis=1)

  #Generate the chroma Dataframe
  for i in range(0,13):
      final_df['mfccs_mean_'+str(i)].loc[j]=mfccs_mean[i]
  for i in range(0,13):
      final_df['mfccs_std_'+str(i)].loc[j]=mfccs_std[i]

  final_df['cent_mean'].loc[j]=np.mean(cent)
  final_df['cent_std'].loc[j]=np.std(cent)
  final_df['cent_skew'].loc[j]=scipy.stats.skew(cent,axis=1)[0]

  contrast_mean=np.mean(contrast,axis=1)
  contrast_std=np.std(contrast,axis=1)

  for i in range(0,7):
      final_df['contrast_mean_'+str(i)].loc[j]=contrast_mean[i]
  for i in range(0,7):
      final_df['contrast_std_'+str(i)].loc[j]=contrast_std[i]
  conts=np.arange(0,7)

  final_df['rolloff_mean'].loc[j]=np.mean(rolloff)
  final_df['rolloff_std'].loc[j]=np.std(rolloff)
  final_df['rolloff_skew'].loc[j]=scipy.stats.skew(rolloff,axis=1)[0]

  final_df['zrate_mean'].loc[j]=np.mean(zrate)
  final_df['zrate_std'].loc[j]=np.std(zrate)
  final_df['zrate_skew'].loc[j]=scipy.stats.skew(zrate,axis=1)[0]

  final_df['tempo'].loc[j]=tempo

final_df.to_csv('dataLevel_1.2.csv')