# python-speech-recognition

Audio transcribing using Python's [SpeechRecognition] library

# Synopsis

```sh
```

# Description

This is my first attempt to transcribe audio files using [SpeechRecognition]
and hopefully guesstimate sentences using [pydub].

It's inherently hard to take a full audio recording of varying length,
accurately convert it to text in fully formed sentences, and provide meta data
on the text such as sentiment or intent. Hopefully this will cover a few of the
goals below.

# Goals

* Provide a full audio transcript for an audio file.
* Make every effort to provide the transcript as sentences, but be aware that
  this will never be accurate as a sentence will be guesstimated based on
  silence / short gaps in conversation.
* Provide sentiment for the transcript.
* Align sentences up with the time they're uttered in the recording.

# Food for thought

* How accurate are the audio transcripts for different speech to text engines?
  * Should multiple speech-to-text APIs be used before settling on one?
  * Should audio transcripts be post processed and fixed by humans?
  * Should the data from APIs that provide alternate transcriptions be stored
    so that users can easily fix their transcriptions?

# Debugging & testing

```sh
# first 30s from an audio file (useful for testing)
ffmpeg -ss 0 -i file.mp3 -t 30 file.wav

# segment audio file into multiple 30s segments (for APIs that cap length)
ffmpeg -i file.wav -f segment -segment_time 30 -c copy parts/out%09d.wav

# serve files in a directory over HTTP
plackup -MPlack::App::Directory -e 'Plack::App::Directory->new(root=>".");' -p 2375
```

# References

* https://github.com/lorgiorepo/python-speech-recognition
* https://stackoverflow.com/questions/36458214/split-speech-audio-file-on-words-in-python/36461422
* https://stackoverflow.com/questions/45526996/split-audio-files-using-silence-detection
* https://www.alexkras.com/transcribing-audio-file-to-text-with-google-cloud-speech-api-and-python/

## Issues

* https://github.com/jiaaro/pydub/issues/169

[pydub]: https://pypi.org/project/pydub/
[SpeechRecognition]: https://pypi.org/project/SpeechRecognition/
