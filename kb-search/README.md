# kb-search

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/kb-search:<TAG>

$ docker push cvdigital/kb-search:<TAG>
```

## Test

```
$ docker run --env KATECHEO_KB='faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json' --env KATECHEO_ARTICLE_ID="article_url" --env KATECHEO_ARTICLE_TITLE_KEY="title" --env KATECHEO_ARTICLE_BODY_KEY="body" --env KATECHEO_SIMILARITY_THRESHOLD="0.15" --name "kb-search" --rm -p 5001:5000 cvdigital/kb-search:<TAG>

$ docker exec -it kb-search python KBSearch_Test.py
```

## Usage

```
$ docker run --env KATECHEO_KB='faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json' --env KATECHEO_ARTICLE_ID="article_url" --env KATECHEO_ARTICLE_TITLE_KEY="title" --env KATECHEO_ARTICLE_BODY_KEY="body" --env KATECHEO_SIMILARITY_THRESHOLD="0.15" --name "kb-search" --rm -p 5001:5000 cvdigital/kb-search:<TAG>

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Can acupuncture help me loose weight?"]}, "meta": {"tags":{"question": true}}}'
```
