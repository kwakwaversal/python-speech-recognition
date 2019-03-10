#!/usr/bin/env python3

# 2019-03-10 - this does not work

import speech_recognition as sr

from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "harvard.wav")

from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent

# https://github.com/jiaaro/pydub/issues/154
def split_on_silencio(audio_segment, min_silence_len=1000, silence_thresh=-16, keep_silence=100):
    """
    audio_segment - original pydub.AudioSegment() object
    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms
    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS
    keep_silence - (in ms) amount of silence to leave at the beginning
        and end of the chunks. Keeps the sound from sounding like it is
        abruptly cut off. (default: 100ms)
    """

    not_silence_ranges = detect_nonsilent(audio_segment, min_silence_len, silence_thresh)

    chunks = []
    for start_i, end_i in not_silence_ranges:
        print("start ", start_i, " end ", end_i)
        start_i = max(0, start_i - keep_silence)
        end_i += keep_silence

        chunks.append(audio_segment[start_i:end_i])

    return chunks

sound_file = AudioSegment.from_wav(AUDIO_FILE)
audio_chunks = split_on_silence(sound_file, 
    # must be silent for at least half a second
    min_silence_len=500,

    # consider it silent if quieter than -16 dBFS
    silence_thresh=-16,

    keep_silence=250
)

for i, chunk in enumerate(audio_chunks):
    out_file = "splitaudio/chunk{0}.wav".format(i)
    print("exporting", out_file)
    chunk.export(out_file, format="wav")

# # use the audio file as the audio source
# r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE) as source:
#     audio = r.record(source)  # read the entire audio file

# # recognize speech using Sphinx
# try:
#     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))
