![alt text](logo.png)

Katecheo is a modular system for topical question answering built on Kubernetes. It is portable to any Kubernetes cluster (in the cloud or on-prem), and it allows developers to integrate state-of-the-art questions answering into their applications via its REST API.  

You can learn more about Katecheo in:

- This [this screencast](https://youtu.be/g51t6eRX2Y8)
- Our [system demonstration paper](https://arxiv.org/abs/1907.00854)

## Deploy Katecheo

### System Prerequisites

Katecheo runs on Kubernetes and utilizes Seldon to serve predictions. You will need:

- A Kubernetes cluster (see [here](https://kubernetes.io/docs/home/) for more information)
- Seldon deployed on the Kubernetes cluster (see [here](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/install.html) for more info about Seldon)
- Ambassator or Istio installed on the Kubernetes cluster (see [here](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/install.html#install-an-ingress-gateway) for more info)

### Data/model Preparation

To classify input messages according to topic, Katecheo requires a pre-trained [spaCy](https://spacy.io/usage/models) NER model trained to detect topical entities. To match topical questions with appropriate knowledge base articles, Katecheo relies on a dataset of knowledge base articles with their corresponding titles.

You will need the following for each topic you want to enable in Katecheo:

- A pre-trained spaCy NER model all bundled into a single zip file
- A JSON file containing Knowledge base articles (structure as shown [here](https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json))

### Deploy

1. Clone this repo.

2. Move into the deploy directory and copy the template configuration file:

    ```
    $ cd deploy && cp config.template.json config.json
    ```

3. Fill in the links to your NER model(s) and knowledge base article files in `config.json`. When you are done, the config file should look something like the following (for a scenario when we are enabling Q&A in two topics: faith, or _Christianity_, and health, or _Medical Sciences_):

    ```
    [
      {
        "name": "faith",
        "ner_model": "https://storage.googleapis.com/pachyderm-neuralbot/ner_models/faith.zip",
        "kb_file": "https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json"
      },
      {
        "name": "health",
        "ner_model": "https://storage.googleapis.com/pachyderm-neuralbot/ner_models/health.zip",
        "kb_file": "https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json"
      }
    ]
    ```

4. Make sure your local `kubectl` is connected to your cluster.

5. Run the deploy script.

    ```
    $ ./deploy.sh
    ```
    
6. This will deploy all of the Katecheo modules to your cluster. Once the Katecheo pod is in a `running` state, you will be able to serve multi-topic answers at the following endpoint: `http://<ingress IP>/seldon/default/katecheo/api/v0.1/predictions`

## Usage

Example request (Question):

```
$ curl -X POST -H 'Content-Type: application/json' -d '{"data": {"names": ["message"], "ndarray": ["What does the Bible say about vegetarianism?"]}}' http://35.201.10.193/seldon/default/katecheo/api/v0.1/predictions
```

Example response (Answer):

```
{
  "meta": {
    "puid": "nf7ukk5cur2dp8bcpe7qe53hsb",
    "tags": {
      "proceed": true,
      "topic": "faith"
    },
    "routing": {
      "target-classifier": -1,
      "question-detector": -1,
      "kb-search": -1
    },
    "requestPath": {
      "target-classifier": "cvdigital/target-classifier:v0.1.0",
      "question-detector": "cvdigital/question-detector:v0.1.0",
      "comprehension": "cvdigital/comprehension:v0.1.0",
      "kb-search": "cvdigital/kb-search:v0.1.0"
    },
    "metrics": []
  },
  "strData": "I think you would be hard pressed to say that the Bible commands a vegetarian diet"
}
```

## Future extensions

In the future we intend to:

- Extend our knowledge base search methodology (e.g., to use bigrams and TF-IDF)
- Enable usage of a wider variety of pre-trained models (BERT, XLNet, etc.)
- Explore other topic matching/modeling techniques to remove our NER model dependency (non-negative matrix factorization and/or latent dirichlet allocation)

## Citing

If you use Katecheo in your research, please cite [Katecheo: A Portable and Modular System for Multi-Topic Question
Answering](https://arxiv.org/abs/1907.00854):

```
@inproceedings{CV2019Katecheo,
  title={Katecheo: A Portable and Modular System for Multi-Topic Question Answering},
  author={Shirish Hirekodi and Seban Sunny and Leonard Topno and Alwin Daniel and Reuben Skewes and Stuart Cranney and Daniel Whitenack},
  year={2019},
  Eprint = {arXiv:1907.00854},
}
```

___
All material is licensed under the [Apache License Version 2.0, January 2004](http://www.apache.org/licenses/LICENSE-2.0).
