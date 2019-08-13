# comprehension

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/reading_comp:0.1

$ docker push cvdigital/reading_comp:0.1
```

## Test

```
$ docker run --name "comprehension" --rm cvdigital/reading_comp:0.1

$ docker exec -it comprehension python ReadingComp_Test.py
```

## Usage

```
$ docker run --name "comprehension" --rm -p 5001:5000 cvdigital/reading_comp:0.1

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["kb", "q"], "ndarray": ["The Matrix is a 1999 science fiction action film written and directed by The Wachowskis, starring Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano.", "Who stars in The Matrix?"]}, "meta": {"tags":{"proceed":true, "topic":"movies"}}}'
```
