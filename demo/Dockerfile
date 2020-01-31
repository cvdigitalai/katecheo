FROM python:3.8.1-slim

EXPOSE 8501

ENV KATECHEO_URL=http://34.89.121.219/seldon/default/katecheo/api/v0.1/predictions

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -r requirements.txt

COPY ./src /src
ENTRYPOINT [ "streamlit", "run"]
CMD ["/src/katecheo.py"]
