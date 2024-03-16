# -*- coding: utf-8 -*-
"""
Created on Wed May 11 21:35:03 2022

@author: HP
"""
import os

os.chdir("drive/My Drive/")

import sys
from aubio import source, notes
from mido import Message, MetaMessage, MidiFile, MidiTrack, second2tick, bpm2tempo
import scipy.io.wavfile as wav

if len(sys.argv) < 3:
    print("Usage: %s <filename> <output> [samplerate]" % sys.argv[0])
    sys.exit(1)


filename = sys.argv[1]
midioutput = sys.argv[2]

downsample = 1
samplerate = 44100 // downsample
if len( sys.argv ) > 3: samplerate = int(sys.argv[3])

win_s = 512 // downsample # fft size
hop_s = 256 // downsample # hop size

import glob
files = glob.glob('/content/drive/My Drive/Project/Level1_5/*')
print(files)
totd=[]

# Capture duration of each file
for e in files:
  file_path = e
  (source_rate, source_sig) = wav.read(file_path)
  duration_seconds = len(source_sig) / float(source_rate)
  totd.append(duration_seconds)

no= len(files)
mydata2= [[]]
test1=[[]]
for i in range(no):
	mydata2.append([])
for i in range(no):
  test1.append([])

def frames2tick(frames, samplerate=samplerate):
      sec = frames / float(samplerate)
      return int(second2tick(sec, ticks_per_beat, tempo))

mydata = []
mydata1= []

c=0
for e in files :
  print(e)
  s = source(e , samplerate, hop_s)
  samplerate = s.samplerate
  tolerance = 0.8
  notes_o = notes("default", win_s, hop_s, samplerate)

  # create a midi file
  mid = MidiFile()
  track = MidiTrack()
  mid.tracks.append(track)
  ticks_per_beat = mid.ticks_per_beat # default: 480
  bpm = 120 # default midi tempo
  tempo = bpm2tempo(bpm)
  track.append(MetaMessage('set_tempo', tempo=tempo))
  track.append(MetaMessage('time_signature', numerator=4, denominator=4))
  last_time = 0
  total_frames = 0
  t1 = []
  while True:
        samples, read = s()
        new_note = notes_o(samples)
        if (new_note[0] != 0):
          note_str = ' '.join(["%.2f" % i for i in new_note])
          d = new_note;
          print("%.6f" % (total_frames/float(samplerate)), d)
          e1 = []
          for e in d :
            e1.append(int(e))
            t1.append((total_frames/float(samplerate), e1[:]))
            delta = frames2tick(total_frames) - last_time
            last_time = frames2tick(total_frames)
          test1[c].append (float("%.6f" % (total_frames/float(samplerate))))
          test1[c].append (int(new_note[0]))
          test1[c].append (int(new_note[1]))
          test1[c].append(int(new_note[2]))
        total_frames += read
        if read < hop_s: break
  #mydata.append(t1)
  mydata2[c].append([t1])
  c=c+1

mfs=[[]]
for i in range(0,no):
  mfs.append([])
k=no

for no in range(0, k):

  n=len(test1[no])
  kn=int(n/4)
  avdur= kn/totd[no]

  #identify the max duration and corrosponding note to find the reference note find the duration of each note
  i=0
  j=4
  dur0=[]

  print("duration of notes")
  while(j<n):
    time = test1[no][j]- test1[no][i]
    dur0.append(round(time,6))
    i=i+4
    j=j+4
  temp= totd[no]-test1[no][i]

  dur0.append(round(temp,6))
  print(dur0)
  maxd=0
  j=1
  k=len(dur0)
  while j<k:
    if (dur0[maxd]==dur0[j]):
      if (test1[no][maxd*4+2]<test1[no][j*4+2]):
        print(test1[no][maxd*4+2])
        print(test1[no][j*4+2])
        maxd=j
    elif (dur0[maxd]<dur0[j]):
      maxd=j
    j=j+1
  print("max dur location")
  print(maxd)
  
  # display reference note
  print("reference note f1")
  print(test1[no][(maxd)*4+1])
  rnote= test1[no][(maxd)*4+1]

  # melodic phrase sequences captured
  phrases =[]
  i=1
  j=i+4
  k=0
  while(j<n):
    temp= test1[no][j]- test1[no][i]
    phrases.append (temp)
    if (test1[no][j+2]==0):
      k=k+1
      phrases.append(100)
    i=i+4
    j=j+4
  print("melodic shifts")
  print(phrases)
  cnt = len(phrases)


  # bigram patterns
  #find increasing by/decreasing by/same note patterns
  #inc 0.1,2,3,4,5,6,7,8,9,10,11,12..21
  #dec 0,1,2,3,4,5,6,7,8,9,10,11,12..21
  #samenote sn inc patterns ip decreasing patterns dp
  inc=[]
  dec=[]
  i=0
  sn=0
  ip=0
  dp=0
  for i in range (0,21):
    inc.append(0)
    dec.append(0)
  i=0
  while (i<cnt-1):
    t= phrases[i+1]
    if (t != 100):
      diff = phrases[i+1]- phrases[i]
      if (diff> -21 and diff <0):
        diff = abs(diff)
        dec[diff]= dec[diff]+1
        dp=dp+1
        flag=-1
      elif (diff==0):
        sn=sn+1
        if (flag ==-1):
          dec[0]=dec[0]+1
        else:
          inc[0]=inc[0]+1
      elif (diff>0 and diff<21):
        ip=ip+1
        inc[diff]=inc[diff]+1
        flag=1
    i=i+1
  print("incresing patterns features 21")
  print(inc)
  print("total f2")
  print(ip)
  print("decreasing patterns features 21")
  print(dec)
  print("total f3")
  print(dp)
  print("total same f4")
  print(sn)

#trigram patterns
# inc inc ii loc 0
# inc dec id loc 1
# dec inc di loc 2
# dec dec dd loc 3
# same same ss loc 4
# same inc si loc 5
# same dec sd loc 6
# inc same is loc 7
# dec same ds loc 8
  trio =[]
  for i in range (0,9):
    trio.append(0)

  i=0
  while (i<cnt-2):
    if ( phrases[i]!= 100 and phrases[i+1] !=100 and phrases[i+2]!=100):
      diff1 = phrases[i+1]- phrases[i]
      diff2= phrases [i+2]- phrases[i+1]
      if (diff1> 0 and diff2 >0):
        trio[0]= trio[0]+1
      elif (diff1> 0 and diff2 <0):
        trio[1]= trio[1]+1
      elif (diff1< 0 and diff2 >0):
        trio[2]= trio[2]+1
      elif (diff1< 0 and diff2 <0):
        trio[3]= trio[3]+1
      elif (diff1== 0 and diff2 ==0):
        trio[4]= trio[4]+1
      elif (diff1== 0 and diff2 >0):
        trio[5]= trio[5]+1
      elif (diff1== 0 and diff2 <0):
        trio[6]= trio[6]+1
      elif (diff1> 0 and diff2 ==0):
        trio[7]= trio[7]+1
      elif (diff1< 0 and diff2 ==0):
        trio[8]= trio[8]+1
    i=i+1
  print("melodic phrases with 3 notes features 9")
  print(trio)

  # find min note , max note and range
  i=1
  j=5
  minnote= test1[no][i]
  maxnote= test1[no][i]
  while(j<n):
    if (minnote>test1[no][j]):
      minnote= test1[no][j]
    j=j+4
  print("minimum note f5")
  print(minnote)
  j=5
  while(j<n):
    if (maxnote<test1[no][j]):
      maxnote= test1[no][j]
    j=j+4
  print("maximum note f6")
  print(maxnote)
  print("note range f7")
  noter= maxnote-minnote
  print(noter)

  # find min intensity , max intensity and range
  i=2
  j=6
  minint= test1[no][i]
  maxint= test1[no][i]
  while(j<n):
    if (minint>test1[no][j]):
      minint= test1[no][j]
    j=j+4
  print("minimum intensity f8")
  print(minint)
  j=5
  while(j<n):
    if (maxint<test1[no][j]):
      maxint= test1[no][j]
    j=j+4
  print("maximum intensity f9")
  print(maxint)
  print("intensity range f10")
  intr= maxint-minint
  print(intr)

  #create melodic feature set
  mfs[no].append(str(round(avdur,4))) #speed of music f0
  mfs[no].append(str(rnote)) # reference note f1
  mfs[no].append(str(ip)) # increasing patterns f2
  mfs[no].append(str(dp)) # decreasing patterns f3
  mfs[no].append(str(sn)) # same note patterns f4
  mfs[no].append(str(minnote)) # minimum note f5
  mfs[no].append(str(maxnote)) # maximim note f6
  mfs[no].append(str(noter)) # note range f7
  mfs[no].append(str(minint)) # minimum intensity f8
  mfs[no].append(str(maxint)) # maximim intensity f9
  mfs[no].append(str(intr)) # intensity range f10

  # increasing patterns 21 f11 to f32
  for i in range (0,21):
    mfs[no].append(str(inc[i]))

  # decreasing patterns 21 f33 to f53
  for i in range (0,21):
    mfs[no].append(str(dec[i]))

  # trio patterns 9 f54 to f62
  for i in range (0,9):
    mfs[no].append(str(trio[i]))
  print("total features")
  print(len(mfs[no]))
print('melodic feature set')
print(mfs)

with open('Level1_5_mfs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(mfs)

from pydub import AudioSegment
sound = AudioSegment.from_mp3("/content/drive/My Drive/dataset/SAD Songs/Sad songs 2/-Woh Kisi Aur Kisi Aur Se Milke-(Mr-Jatt.com).mp3")
sound.export("/content/drive/My Drive/dataset/SAD Songs/test.wav", format="wav")
