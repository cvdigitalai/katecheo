# Katecheo

Katecheo is a modular system for topical question answering built on Kubernetes. It is portable to any Kubernetes cluster (in the cloud or on-prem), and it allows developers to integrate state-of-the-art questions answering into their applications via its REST API.  

You can learn more about Katecheo in:

- This blog post
- other

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
$ kubectl apply -f comprehension/deployment.json

$ kubectl apply -f target-classifier/deployment.json

$ kubectl apply -f kb-search/deployment.json

$ kubectl apply -f question-detector/deployment.json
```

## Authentication

coming soon...

## Future extensions

In the future we intend to:

- Document how Katecheo can be used for multi-topic question answering
- Extend topic classification beyond the currently methodology, which relies on spacy NER models
- Integrate full text search for knowledge base article matching
