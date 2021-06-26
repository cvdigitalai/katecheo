# kb-search

## Build

```
$ docker build -t cvdigital/kbsearch:<TAG> .

$ docker push cvdigital/kbsearch:<TAG>
```

## Test

```
$ docker run -d -p 6070:6070 --network="ice-net" --env KATECHEO_KB='faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json' --env KATECHEO_ARTICLE_ID="article_url" --env KATECHEO_ARTICLE_TITLE_KEY="title" --env KATECHEO_ARTICLE_BODY_KEY="body" --env KATECHEO_SIMILARITY_THRESHOLD="0.15" --name "kbsearch" cvdigital/kbsearch:<TAG>

$ docker exec -it kbsearch python3 KBSearch_Test.py
```

## Develop

- **Prep**

  `docker network ls, docker network create -d bridge ice-net`

- **Install**

  `$ pip3 install -r requirements.py`

- **Start in local environment**

  `$ ./run-app-for-unit-test.sh`

- **Unit test**

  `$ python3.6 KBSearch_Test.py`
```
