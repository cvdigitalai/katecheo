# kb-search

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/kb_search:v0.02
$ docker push cvdigital/kb_search:v0.02
```

## Test

```
$ docker run --env KATECHEO_KB='health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json,faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json' --name "kb-search" --rm cvdigital/kb_search:v0.02
$ docker exec -it <CONTAINER_ID> python KBSearch_Test.py
```
