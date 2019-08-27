# kb-search

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/kb_search:<TAG>

$ docker push cvdigital/kb_search:<TAG>
```

## Test

```
$ docker run --env KATECHEO_KB='health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json,faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json' --name "kb-search" --rm cvdigital/kb_search:<TAG>

$ docker exec -it kb-search python KBSearch_Test.py
```

## Usage

```
$ docker run --env KATECHEO_KB='health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json,faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json' --name "kb-search" --rm -p 5001:5000 cvdigital/kb_search:<TAG>

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}, "meta": {"tags":{"proceed":true, "topic": "health"}}}'
```
