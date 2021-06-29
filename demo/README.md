# Streamlit demo app for Katecheo

This is demo web app (powered by [Streamlit](https://streamlit.io)) that demonstrates an example integration of Katecheo. It also allows users to utilize Katecheo via a simply browser-based interface to test answers and show off their cool question answering system!

## Run the demo via Docker

The easiest way to run the app is via Docker. Run the following command replacing `<Katecheo IP>` with the IP of your Katecheo deployment:

```
$ docker run -it -p 8501:8501 --env KATECHEO_URL="<KATECHEO URL>" cvdigital/katecheo-demo:v0.2.1
```

You can then navigate to `http://<your IP, e.g., localhost>:8501` to interact with the app.

## Build the Docker image

Clone the repo:

```sh
$ git clone git@github.com:cvdigitalai/katecheo.git
```

Navigate to the demo directory:

```
$ cd katecho/demo/
```

Build the docker image:

```
$ docker build -t cvdigital/katecheo-demo:<VERSION> .
```
