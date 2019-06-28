# kb-search

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/kb_search:v0.02
$ docker push cvdigital/kb_search:v0.02
```

## Test

```
$ docker run -it cvdigital/kb_search:v0.02 --rm -p 5001:5000
$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}}'
```
