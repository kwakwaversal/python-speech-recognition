FROM python:3.6

MAINTAINER Paul Williams <kwakwaversal@gmail.com>

WORKDIR /opt/tokenize-and-transcribe

COPY requirements.txt ./
RUN apt-get -y update && apt-get -y install build-essential \
    libpulse-dev \
    swig \
    libasound2-dev \
    ffmpeg

# auditok
RUN apt-get -y install portaudio19-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "./tokenize_and_transcribe.py", "samples/harvard.wav"]
