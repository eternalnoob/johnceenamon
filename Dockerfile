FROM ubuntu:18.04

MAINTAINER Ethan Seither "ethan.seither@gmail.com"

RUN apt update && apt install -y python3.7 python3-pip

RUN apt install -y libffi-dev libnacl-dev python3-dev libopus-dev ffmpeg

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

RUN python3 -m pip install -U discord.py[voice]

COPY . /

ENTRYPOINT [ "python3" ]
CMD [ "basic_voice.py" ]
