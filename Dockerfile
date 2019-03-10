FROM python:3.6

MAINTAINER Paul Williams <kwakwaversal@gmail.com>

WORKDIR /opt/python-speech-recognition

COPY requirements.txt ./
RUN apt-get -y update && apt-get -y install build-essential \
    libpulse-dev \
    swig \
    libasound2-dev \
    ffmpeg
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "./init.py"]
