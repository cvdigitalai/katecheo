# comprehension

## To build

From this comprehension directory:

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 dwhitena/reading_comp:0.1

$ docker push dwhitena/reading_comp:0.1
```

## API

Example request:

```
$ curl -X POST -H 'Content-Type: application/json' \
    -d '{"data": {"names": ["kb", "q"], "ndarray": ["The Matrix is a 1999 science fiction action film written and directed by The Wachowskis, starring Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano.", "Who stars in The Matrix?"]}}' \
    http://35.201.10.193/seldon/default/reading-comprehension/api/v0.1/predictions
```

Example response:

```
{
  "meta": {
    "puid": "qihufcdu7dejkgrvu300ml7iv8",
    "tags": {
    },
    "routing": {
    },
    "requestPath": {
      "classifier": "dwhitena/reading_comp:0.1"
    },
    "metrics": []
  },
  "strData": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving, and Joe Pantoliano"
}
```

