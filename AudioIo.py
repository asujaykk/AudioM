#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 11:30:25 2021

@author: akhil_kk
"""

import pyaudio
import wave
import os
import numpy as np
# Set chunk size of 1024 samples per data frame
# chunk = 128 # Record in chunks of 1024 samples
# sample_format = pyaudio.paInt16  # 16 bits per sample
# out_channels = 2
# in_channels=2
# fs = 16000  # Record at 44100 samples per second
# seconds = 1



#print('Recording')

class AudioIoM():    
    def __init__(self,chunk = 128,fs = 16000,in_channels=2,out_channels = 2,sample_format = pyaudio.paFloat32):
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.chunk=chunk
        self.fs=fs
        self.in_channels=in_channels
        self.out_channels=out_channels
        self.sample_format=sample_format
        
        self.stream_i = self.p.open(format=sample_format,
                        channels=in_channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        self.stream_o = self.p.open(format=sample_format,
                        channels=out_channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        output = True)   

        print("Audio input and output streams created")
        
    
    def Set_Out_Volume(self,volume):
        resp=os.popen("amixer -D pulse sset Master "+str(volume)+"%").read()
        return int(resp[resp.find('[')+1:resp.find('%')])
    
    def Set_In_Volume(self,volume):
        resp=os.popen("amixer -D pulse sset Capture "+str(volume)+"%").read()
        return int(resp[resp.find('[')+1:resp.find('%')])
    
    def Get_Out_Volume(self):
        resp=os.popen("amixer -D pulse sget Master ").read()
        return int(resp[resp.find('[')+1:resp.find('%')])
    
    def Get_In_Volume(self):
        resp=os.popen("amixer -D pulse sget Capture ").read()
        return int(resp[resp.find('[')+1:resp.find('%')])
    
    
    def Save_Wave_File(self,filename,frames):
        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.out_channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def Read_Wave_File(self,filename):
        wf = wave.open(filename, 'rb')
        frames=[]
        rd_data = wf.readframes(self.chunk)
        while rd_data != '':
            frames.append(rd_data)
            rd_data = wf.readframes(self.chunk)
        return frames

    
    def Record(self,duration):
        frames=[]
        for i in range(0, int(self.fs / self.chunk * duration)):
            data = self.stream_i.read(self.chunk)

            frames.append(data)
        return frames

    def Record_np_array(self,duration):
        frames=np.empty((self.in_channels,1),np.float32)
        for i in range(0, int(self.fs / self.chunk * duration)-1):       # here -1 is to avoid 16001 sample due to concat operatio
            frames= np.concatenate((frames,self.decode(self.stream_i.read(self.chunk)).T),1)
        return frames


    def Play(self,frames,duration):
        for i in range(0, int(self.fs / self.chunk * duration)):
            data = frames[i]
            self.stream_o.write(data)
    
    
    
    def decode(self,in_data):
        """
        Convert a byte stream into a 2D numpy array with 
        shape (chunk_size, channels)
    
        Samples are interleaved, so for a stereo stream with left channel 
        of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output 
        is ordered as [L0, R0, L1, R1, ...]
        """
        # TODO: handle data type as parameter, convert between pyaudio/numpy types
        result = np.frombuffer(in_data, dtype=np.float32)
    
        #chunk_length = len(result) / channels
        #assert chunk_length == int(chunk_length)
    
        result = np.reshape(result, (self.chunk, self.in_channels))
        return result


    def encode(self,signal):
        """
        Convert a 2D numpy array into a byte stream for PyAudio
    
        Signal should be a numpy array with shape (chunk_size, channels)
        """
        interleaved = signal.flatten()
    
        # TODO: handle data type as parameter, convert between pyaudio/numpy types
        out_data = interleaved.astype(np.float32).tostring()
        return out_data

    
    def __delete__(self):
        self.stream_i.stop_stream()
        self.stream_o.stop_stream()
        self.stream_i.close()
        self.stream_o.close()
        # Terminate the PortAudio interface
        self.p.terminate()
