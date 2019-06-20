# question-detector

## To build

From this comprehension directory:

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 dwhitena/question-detector:v0.1

$ docker push dwhitena/question-detector:v0.1
```

## API

Example request:

```
$ curl -X POST -H 'Content-Type: application/json' \
    -d '{"data": {"names": ["message"], "ndarray": ["What does the Bible say about tattoos"]}}' \
    http://35.201.10.193/seldon/default/question-detector/api/v0.1/predictions
```

Example response:

```
{
  "meta": {
    "puid": "q2nc7mbs08nuabtt7h6ma84g1s",
    "tags": {
    },
    "routing": {
    },
    "requestPath": {
      "classifier": "dwhitena/question-detector:v0.1"
    },
    "metrics": []
  },
  "strData": "{\"text\": \"what does the bible say about tattoos ?\", \"question\": true}"
}
```

