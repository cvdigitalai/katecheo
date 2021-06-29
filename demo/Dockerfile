FROM python:3.8.1-slim

EXPOSE 8501

ENV KATECHEO_URL=https://katecheo-route-katecheo.apps.ice-staging.cfdf.p2.openshiftapps.com/questiondetector
# ENV KATECHEO_KB_TOPICS="topic_1;topic_2"

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -r requirements.txt

COPY ./src /src
ENTRYPOINT [ "streamlit", "run"]
CMD ["/src/katecheo.py"]
