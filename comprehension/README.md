# comprehension

## Build

```
$ docker build . -f Dockerfile -t seldonio/seldon-core-transformers-base:0.1

$ s2i build . seldonio/seldon-core-transformers-base:0.1 cvdigital/comprehension:<TAG>

$ docker push cvdigital/comprehension:<TAG>
```

## Test

```
$ docker run --name "comprehension" --rm cvdigital/comprehension:<TAG>

$ docker exec -it comprehension python ReadingComp_Test.py
```

## Usage

```
$ docker run --name "comprehension" --rm -p 5001:5000 cvdigital/comprehension:<TAG>

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["kb", "q"], "ndarray": ["The Matrix is a 1999 science fiction action film written and directed by The Wachowskis, starring Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano.", "Who stars in The Matrix?"]}, "meta": {"tags":{"on_topic": true, "article_source": "http://somesite.com", "kb_search_error":""}}}'
```
