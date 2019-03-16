FROM python:3.6

MAINTAINER Paul Williams <kwakwaversal@gmail.com>

WORKDIR /opt/tokenize-and-transcribe

# build tools
RUN apt-get -y update && apt-get -y install build-essential

# auditok
RUN apt-get -y install portaudio19-dev

# PockerSphinx
RUN apt-get -y install swig libpulse-dev

# pydub
RUN apt-get -y install ffmpeg

# install packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["python3", "./tokenize_and_transcribe.py", "samples/harvard.wav"]
ENTRYPOINT ["python3", "./tokenize_and_transcribe.py"]
