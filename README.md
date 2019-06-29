![alt text](Katecho_logo.png)

Katecheo is a modular system for topical question answering built on Kubernetes. It is portable to any Kubernetes cluster (in the cloud or on-prem), and it allows developers to integrate state-of-the-art questions answering into their applications via its REST API.  

You can learn more about Katecheo in:

- This this screencast
- Our EMNLP 2019 system submission (coming soon)

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

### Deploy Katecheo

1. Clone this repo.

2. Move into the deploy directory and copy the template configuration file:

    ```
    $ cd deploy && cp config.template.json config.json
    ```

3. Fill in the links to your NER model(s) and knowledge base article files in `config.json`. When you are done, the config file should look something like the following (for a scenario when we are enabling Q&A in two topics: faith, or Christianity, and health, or Medical Sciences):

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

4. blah
    

## Future extensions

In the future we intend to:

- Document how Katecheo can be used for multi-topic question answering
- Extend topic classification beyond the currently methodology, which relies on spacy NER models
- Integrate full text search for knowledge base article matching

___
All material is licensed under the [Apache License Version 2.0, January 2004](http://www.apache.org/licenses/LICENSE-2.0).
