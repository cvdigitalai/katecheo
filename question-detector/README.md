# question-detector

## Build

```
$ docker build -t cvdigital/questiondetector:<TAG> .

$ docker push cvdigital/questiondetector:<TAG>
```

## Test

```
$ docker run -d -p 6060:6060 --network="ice-net" --name "questiondetector" cvdigital/questiondetector:<TAG>

# docker exec -it questiondetector python3 QuestionDetector_Test.py
```

## Usage

```
$ docker run -d -p 6060:6060 --network="ice-net" --name "questiondetector" cvdigital/questiondetector:<TAG>

$ curl -X POST -H 'Content-Type: application/json' -d '{"params": "Can acupuncture help me loose weight?"}' http://localhost:6060/questiondetector
```

## Develop

- **Prep**

  `docker network ls, docker network create -d bridge ice-net`

- **Install**

  `$ pip3 install -r requirements.py`

- **Start in local environment**

  `$ python3.6 QuestionDetector.py`

- **Unit test**

  `$ python3.6 QuestionDetector_Test.py`
```
