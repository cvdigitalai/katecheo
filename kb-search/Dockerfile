FROM ubuntu:18.04
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install python3.6 -y
RUN apt-get install python3.6-dev -y
RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 KBSearch.py
