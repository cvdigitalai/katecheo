# comprehension

## Build

```
$ docker build -t cvdigital/comprehension:<TAG> .

$ docker push cvdigital/comprehension:<TAG>

```

## Test

```
$ docker run -d -p 6080:6080 --network="ice-net" --name "comprehension" cvdigital/comprehension:<TAG>

$ docker exec -it comprehension python3 ReadingComp_Test.py
```

## Develop

- **Prep**

  `docker network ls, docker network create -d bridge ice-net`

- **Install**

  `$ pip3 install -r requirements.py`

- **Start in local environment**

  `$ python3.6 ReadingComp.py`

- **Unit test**

  `$ python3.6 ReadingComp_Test.py`
