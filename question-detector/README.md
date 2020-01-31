# question-detector

## Build

```
$ s2i build . seldonio/seldon-core-s2i-python37:0.10 cvdigital/question-detector:<TAG>

$ docker push cvdigital/question-detector:<TAG>
```

## Test

```
$ docker run --name "question-detector" --rm cvdigital/question-detector:<TAG>

# docker exec -it question-detector python QuestionDetector_Test.py
```

## Usage

```
$ docker run --name "question-detector" --rm -p 5001:5000 cvdigital/question-detector:<TAG>

$ curl -g http://localhost:5001/predict --data-urlencode 'json={"data": {"names": ["message"], "ndarray": ["Does some food increase pollen allergy symptoms?"]}}'
```
