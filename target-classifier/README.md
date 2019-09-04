# target-classifier

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python37:0.10 cvdigital/target-classifier:0.1

$ docker push cvdigital/target-classifier:0.1
```

## Test

```
$ docker run --env KATECHEO_NER='health=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/health.zip,faith=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/faith.zip' --name "target-classifier" --rm cvdigital/target-classifier:0.1

$ docker exec -it target-classifier python TargetClassifier_Test.py
```

## Usage

```
$ docker run --env KATECHEO_NER='health=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/health.zip,faith=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/faith.zip' --name "target-classifier" --rm -p 5001:5000 cvdigital/target-classifier:0.1

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}, "meta": {"tags":{"question":true}}}'
```
