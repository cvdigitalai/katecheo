# target-classifier

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/target-classifier-multi:v0.1
$ docker push cvdigital/target-classifier-multi:v0.1
```

## Test

```
$ docker run --env KATECHEO_NER='health=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/health.zip,faith=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/faith.zip' --rm cvdigital/target-classifier-multi:v0.1
$ docker exec -it <CONTAINER_ID> python TargetClassifier_Test.py
```

## Usage

```
$ docker run --env KATECHEO_NER='health=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/health.zip,faith=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/faith.zip' --rm -p 5001:5000 cvdigital/target-classifier-multi:v0.1
$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}, "meta": {"tags":{"proceed":true}}}'
```
