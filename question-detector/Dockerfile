FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 QuestionDetector.py
