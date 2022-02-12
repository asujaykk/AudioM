# AudioM
A module designed for audio processing : audio recording and basic feature extraction
1. AudioIo.py: This module contain "AudioIoM" class designed for various audio IO functionality, The class methods are explaned below
   1. Record : Record audio from microphone for a given duration (duration in seconds)
   2. Play : Play the audio frames (The playing duration parameter determine the playing speed, ideally this duration should match the recorded duration)
   3. Read_Wave_File:  To read audio from a wave file in the disk
   4. Save_Wave_File: To save audio frames to a wave file.
   5. Set_Out_Volume:  To set Audio output volume (argument value range: 0-100 %)
   6. Set_In_Volume : To set Audio input (mic gain) volume (argument value range: 0-100 %)
   7. Get_Out_Volume : To read the current Audio output volume 
   8. Get_In_Volume : To read the current Audio input volume 
  
2. AudioProc.py : This module contain methods for basic audio feature extraction (python module librosa used for feature extraction)
   1. Load_Audio : For loading wave file from disk for processing (can be mono or stereo)
   2. Get_Rms_Stereo : To get Root Mean Square value of stereo audio
   3. Get_Zcr_Stereo : To get Zero Crossing Rate value of stereo audio
   4. Get_Rms_Diff : To get RMS difference of stereo channel (Majorly for DOA application)
   5. Get_Rms : To get Root Mean Square value of mono audio
   6. Get_Zcr : To get Zero Crossing Rate value of mono audio
