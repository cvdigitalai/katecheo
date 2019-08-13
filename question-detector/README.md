# question-detector

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python37:0.10 cvdigital/question-detector:0.1
$ docker push cvdigital/question-detector:0.1
```

## Test

```
$ docker run --name "question-detector" --rm cvdigital/question-detector:0.1
# docker exec -it question-detector python QuestionDetector_Test.py
```

## Usage

```
$ docker run --name "question-detector" --rm -p 5001:5000 cvdigital/question-detector:0.1
$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}}'
```
