# comprehension

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/reading_comp:0.1
$ docker push cvdigital/reading_comp:0.1
```

## Test

```
$ docker run --rm cvdigital/reading_comp:0.1
$ docker exec -it <CONTAINER_ID> python ReadingComp_Test.py
```

## Usage

```
$ docker run --env --rm -p 5001:5000 cvdigital/reading_comp:0.1
$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}, "meta": {"tags":{"proceed":true}}}'
```
