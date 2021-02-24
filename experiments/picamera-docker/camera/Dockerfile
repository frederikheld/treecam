# FROM python:3.9-buster
FROM balenalib/raspberry-pi-debian:latest
# FROM lukechilds/dockerpi:latest

RUN apt-get update && \
    apt-get upgrade -y

RUN apt-get install python3 python3-pip

RUN python3 --version
RUN pip3 --version

RUN pip3 install picamera

WORKDIR /usr/src/app

VOLUME ["/opt/vc", "/usr/src/app"]

# COPY scripts .

CMD ["sh", "start.sh"]
