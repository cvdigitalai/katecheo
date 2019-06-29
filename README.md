![alt text](Katecho_logo.png)

Katecheo is a modular system for topical question answering built on Kubernetes. It is portable to any Kubernetes cluster (in the cloud or on-prem), and it allows developers to integrate state-of-the-art questions answering into their applications via its REST API.  

You can learn more about Katecheo in:

- This this screencast
- Our EMNLP 2019 system submission (coming soon)

## Deploy Katecheo

### System Prerequisites

Katecheo runs on Kubernetes and utilizes Seldon to serve predictions. You will need:

- A Kubernetes cluster (see here for more information)
- Seldon deployed on the Kubernetes cluster (see here for more info about Seldon)
- Ambassator or Istio installed on the Kubernetes cluster (see here for more info)

### Data/model Preparation

To (optionally) classify input messages according to topic, Katecheo required a pre-trained spacy NER model trained to detect topical entities. To match topical questions with appropriate knowledge base articles, Katecheo relies on a data set of knowledge base articles with their corresponding titles.

In summary, you will need:

- A pre-trained spacy NER model (see this tutorial to create a custom NER model with spacy)
- A JSON file containing Knowledge base articles (structure as shown here)

### Deploy KubeQuest

```
$ cd deploy && ./deploy.sh
```

## Future extensions

In the future we intend to:

- Document how Katecheo can be used for multi-topic question answering
- Extend topic classification beyond the currently methodology, which relies on spacy NER models
- Integrate full text search for knowledge base article matching

___
All material is licensed under the [Apache License Version 2.0, January 2004](http://www.apache.org/licenses/LICENSE-2.0).
