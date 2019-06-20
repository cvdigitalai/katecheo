# kb-search

## To build

From this comprehension directory:

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/gq_search:v0.02

$ docker push cvdigital/gq_search:v0.02
```

## API

Example request:

```
$ curl -X POST -H 'Content-Type: application/json' \
    -d '{"data": {"names": ["kb", "q"], "ndarray": ["What does the Bible say about tattoos"]}}' \
    http://35.201.10.193/seldon/default/gq-search/api/v0.1/predictions
```

Example response:

```
{
  "meta": {
    "puid": "vs2episkdug9l1mloilmht4uqa",
    "tags": {
    },
    "routing": {
    },
    "requestPath": {
      "classifier": "cvdigital/gq_search:v0.02"
    },
    "metrics": []
  },
  "strData": "{\"id\": \"666\", \"confidence\": 99, \"article_title\": \"What does the Bible say about tattoos?\"}"
}
```

