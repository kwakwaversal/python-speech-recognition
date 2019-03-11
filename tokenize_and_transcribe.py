#!/usr/bin/env python3

"""transcribe audio segments

This script has been thrown together after a few days research to convert audio
files (wavs) containing speech, and transcribe them using the offline
speech-to-text engine PocketSphinx. It uses auditok to identify the regions of
interest.

It uses the `SpeechRecognition` package to perform the speech transcribing so
it could be easily extended to use a more accurate engine.

JSON output with a breakdown of each audio segment is returned to STDOUT with
enough metadata to be useful and sentiment analysis from `textblob`.

"""

import os
import json
import speech_recognition as sr
import sys
from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer
from pathlib import Path
from pydub import AudioSegment
from textblob import TextBlob

def transcribe_audio(file):
    path = Path(file)

    tempsound = AudioSegment.from_wav(file)
    tempsound = tempsound.set_channels(1)
    tempsound.export('0wavtmp_'+path.name, format="wav")
    tmpfile = '0wavtmp_'+path.name

    # We set the `record` argument to True so that we can rewind the source
    asource = ADSFactory.ads(filename=tmpfile, record=True)

    validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=50)

    # Default analysis window is 10 ms (float(asource.get_block_size()) / asource.get_sampling_rate())
    # min_length=20 : minimum length of a valid audio activity
    # max_length=500 :  maximum length of a valid audio activity
    # max_continuous_silence=30 : maximum length of a tolerated silence within valid audio activity window
    tokenizer = StreamTokenizer(validator=validator, min_length=20, max_length=500, max_continuous_silence=30)

    asource.open()
    tokens = tokenizer.tokenize(asource)
    r = sr.Recognizer()

    json_output = {
        "segments": []
    }

    for index,t in enumerate(tokens):
        # print("Token starts at {0} and ends at {1}".format(t[1] * 10, t[2] * 10))
        newAudio = AudioSegment.from_wav(file)
        newAudio = newAudio[t[1] * 10:t[2] * 10] 

        chunk_name = "{}_clip{}.wav".format(path.stem,index)
        # print("Generating", chunk_name)
        newAudio.export(chunk_name, format="wav")
        with sr.AudioFile(chunk_name) as source:
            audio = r.record(source)

        # recognize speech using Sphinx
        try:
            transcription = r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        tb = TextBlob(transcription)

        json_output['segments'].append({
            "start": t[1] * 10,
            "end": t[2] * 10,
            "transcription": transcription,
            "sentiment": {
                "polatirty": tb.polarity,
                "subjectivity": tb.subjectivity
            }
        })

    print(json.dumps(json_output))

    os.remove(tmpfile)

if len(sys.argv) < 2:
    print("You failed to provide a filename to tokenize")
    sys.exit(1)

filename=sys.argv[1]
transcribe_audio(filename) 
