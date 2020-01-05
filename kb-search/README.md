# kb-search

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.10 cvdigital/kb_search:<TAG>

$ docker push cvdigital/kb_search:<TAG>
```

## Test

```
$ docker run --env KATECHEO_KB='faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json' --env ARTICLE_ID="article_url" --env ARTICLE_TITLE_KEY="title" --env ARTICLE_BODY_KEY="body" --env COSINE_SIMILARITY_THRESHOLD="0.19" --name "kb-search" --rm -p 5001:5000 cvdigital/kb_search:<TAG>

$ docker exec -it kb-search python KBSearch_Test.py
```

## Usage

```
$ docker run --env KATECHEO_KB='faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json' --env ARTICLE_ID="article_url" --env ARTICLE_TITLE_KEY="title" --env ARTICLE_BODY_KEY="body" --env COSINE_SIMILARITY_THRESHOLD="0.19" --name "kb-search" --rm -p 5001:5000 cvdigital/kb_search:<TAG>

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Can acupuncture help me loose weight?"]}, "meta": {"tags":{"question": true}}}'
```
