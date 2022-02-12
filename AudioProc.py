#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:11:52 2021

@author: akhil_kk
"""
# Common audio feature extraction module for audio data processing

import librosa
import numpy as np

fr_l=512 #frame length
#To load an audio wave file  
def Load_Audio(audio_file_name,sr=None,mono=False): #default framelength is 512 in rms claculation        
    # sr=None to use original sample rate
    aud_stereo, sr = librosa.load(audio_file_name, sr=None, mono=mono)
    return aud_stereo, sr
 
#To get rms value of both channel, input should be numpy array (two channel)       
def Get_Rms_Stereo(aud_stereo):
    rms_left = Get_Rms(aud_stereo[0, :])
    rms_right = Get_Rms(aud_stereo[1, :])

    rms = np.concatenate((rms_left,rms_right), 0)
    return rms

#To get zero crossing rate of two channels
def Get_Zcr_Stereo(aud_stereo):    
    zcr_left = Get_Zcr(aud_stereo[0, :])
    zcr_right = Get_Zcr(aud_stereo[1, :])

    zcr = np.concatenate((zcr_left,zcr_right), 0)    
    return zcr

#To get Root Means Square diffetrence of two channels (This implementation is meant for DOA (Direction Of Arrival) )
def Get_Rms_Diff(rms_two_channel):
    return (rms_two_channel[0,:]-rms_two_channel[1,:])

#To get rms value of one channel
def Get_Rms(aud_mono,frame_length=fr_l):
    return librosa.feature.rms(aud_mono, frame_length)
        
#To get zero crossing rate of one channels    
def Get_Zcr(aud_mono,frame_length=fr_l):
    return librosa.feature.zero_crossing_rate(aud_mono, frame_length)
