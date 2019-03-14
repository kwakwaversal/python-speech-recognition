# coding: utf-8

import math
import base64
import httplib2
from pydub import AudioSegment
from pydub.silence import detect_silence

import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


#######################################################################################
def timecode_convert(time):
    time_float = round(time - math.floor(time),3)
    time_int = math.floor(time)
    
    #Float
    if time_float == 0:
        str_float = "000"
    else:
        str_float = str(time_float)
        str_float = str_float[2:]
    
    #second
    if time_int < 60:
        time_sec = time_int
    else:
        time_sec = time_int%60
    
    if time_sec != 0:
        if time_sec < 10:
            str_sec = "0" + str(int(time_sec))
        else:
            str_sec = str(int(time_sec))
    else:
        str_sec = "00"
        
    #minuits
    time_min = math.floor(time_int/60)
    if time_min < 60:
        _time_min = time_min
    else:
        _time_min = time_min%60

    if _time_min != 0:
        if _time_min < 10:
            str_min = "0" + str(int(_time_min))
        else:
            str_min = str(int(_time_min))
    else:
        str_min = "00"
    
    #Hour
    time_hor = math.floor(time_min/60)
    
    if time_hor != 0:
        if time_hor < 10:
            str_hor = "0" + str(int(time_hor))
        else:
            str_hor = str(int(time_hor))
    else:
        str_hor = "00"
    

    return str_hor + ":" + str_min + ":" + str_sec + "," + str_float
#####################################################################################



if __name__ == '__main__':

    client = speech.SpeechClient()

    audio_data = []
    duration_data = []
    duration_data.append(0.0)
    timecode = 0
    
    sound = AudioSegment.from_file('./sample_01mono_short.wav', format='wav')
    silent_ranges = detect_silence(sound, min_silence_len=800, silence_thresh=-40)
    
    for i in range(len(silent_ranges)):
        if i == 0:
            chunk = sound[0:silent_ranges[i][1]]
        elif i == (len(silent_ranges) - 1):
            chunk = sound[0:silent_ranges[i][1]:]
        else:
            chunk = sound[silent_ranges[i-1][1]:silent_ranges[i][1]]
        
        chunk.export('./temp5.wav', format='wav')
        AUDIO_FILE = "./temp5.wav"
        
        duration = chunk.duration_seconds
        timecode = timecode + duration
        duration_data.append(timecode)

        with io.open(AUDIO_FILE, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
            audio_data.append(audio)

    with open('OUTPUT3.srt', 'w') as g:
        for i in range(len(audio_data)):
            print(timecode_convert(duration_data[i]))
            g.write(str(i + 1))
            g.write('\n')
            ################################################################################################################
            if i == 0:
                g.write(str(timecode_convert(duration_data[i])) + " --> " + str(timecode_convert(duration_data[i + 1])))
            else:
                g.write(str(timecode_convert(duration_data[i])) + " --> " + str(timecode_convert(duration_data[i + 1] - 1)))
            ################################################################################################################
            g.write('\n')

            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=44100,
                language_code='ja-JP')

            response = client.recognize(config, audio_data[i])

            for result in response.results:
                try:
                    text = result.alternatives[0].transcript
                    print text 
                    g.write(text.encode('utf-8'))
                except:
                    print "@@@@@@@@@@@@@@@@@@@@@@"
                    g.write("@@@@@@@@@@@@@@@@@@@@@@")
                g.write('\n')
                g.write('\n')

