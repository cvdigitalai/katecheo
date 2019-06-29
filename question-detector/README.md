# question-detector

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python3:0.7 cvdigital/question-detector:v0.02
$ docker push cvdigital/question-detector:v0.02
```

## Test

```
$ docker run --rm cvdigital/question-detector:v0.02
# docker exec -it <CONTAINER_ID> python QuestionDetector_Test.py
```

## Usage

```
$ docker run --env --rm -p 5001:5000 cvdigital/question-detector:v0.02
$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}}'
```
