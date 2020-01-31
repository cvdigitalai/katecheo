![alt text](logo.png)

Katecheo is a modular system for topical question answering built on Kubernetes. It is portable to any Kubernetes cluster (in the cloud or on-prem), and it allows developers to integrate state-of-the-art questions answering into their applications via its REST API.  

Check out [this screencast](https://youtu.be/dyhkLuq4Lo8) to see Katecheo in action!

## Deploy Katecheo

### System Prerequisites

Katecheo runs on Kubernetes and utilizes Seldon to serve predictions. You will need:

- A Kubernetes cluster (see [here](https://kubernetes.io/docs/home/) for more information)
- Seldon deployed on the Kubernetes cluster (see [here](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/install.html) for more info about Seldon)
- Ambassator or Istio installed on the Kubernetes cluster (see [here](https://docs.seldon.io/projects/seldon-core/en/latest/workflow/install.html#install-an-ingress-gateway) for more info)

### Data/model Preparation

To match topical questions with appropriate knowledge base articles, Katecheo relies on one or more sets of knowledge base articles (one per topic of interest, e.g., one for sports or one for health). For each topic you want to enable in Katecheo, you will need a JSON file containing Knowledge base articles (structure as shown [here](https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_medical_small.json))

### Deploy

1. Clone this repo.

2. Move into the deploy directory and copy the template configuration file:

    ```
    $ cd deploy && cp config.template.json config.json
    ```

3. Modify the `config.json` file according to your deployment by, at the minimum, filling in the links to your knowledge base article files and the field names representing your article IDs, article titles, and article bodies in the article files. You can also optionally modify the similarity threshold used by Katecheo when matching quesitons to articles and the comprehension model used by Katecheo (either `bert` or `bidaf`). When you are done, the config file should look something like the following (for a scenario when we are enabling Q&A in two topics: _Christianity_ and _Medical Sciences_):

    ```
    {
        "article_id": "title",
        "article_title_key": "title",
        "article_body_key": "body",
        "similarity_threshold": "0.15",
        "comprehension_model": "bert",
        "model": [
            {
                "name": "Christianity",
                "kb_file": "https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_christianity_small.json"
            },
            {
                "name": "Medical Sciences",
                "kb_file": "https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_medical_small.json"
            }
        ]
    }
    ```

4. Make sure your local `kubectl` is connected to your cluster.

5. Run the deploy script.

    ```
    $ ./deploy.sh
    ```
    
6. This will deploy all of the Katecheo modules to your cluster. Once the Katecheo pod is in a `running` state, you will be able to serve multi-topic answers at the following endpoint: `http://<ingress IP>/seldon/default/katecheo/api/v0.1/predictions`. You can usually find the `<ingress IP>` using the `kubectl get svc` command and looking for the public IP for, e.g., ambassador. 

## Usage

### Via REST API 

Example request (Question):

```
$ curl -X POST -H 'Content-Type: application/json' -d '{"data": {"names": ["message"], "ndarray": ["How should you treat people with high risk factors for coronary heart disease?"]}}' http://<ingress IP>/seldon/default/katecheo/api/v0.1/predictions
```

Example response (Answer):

```
{
  "meta": {
    "puid": "lftagepuvbpskvhaudpb4a8b14",
    "tags": {
      "article_id": "Can Prediabetes cause coronary heart disease?",
      "comprehension_error": "",
      "comprehension_model": "BERT",
      "kb_search_error": "",
      "on_topic": true,
      "question": true,
      "question_detector_error": "",
      "topic": "Medical Sciences"
    },
    "routing": {
      "question-detector": -1,
      "kb-search": -1
    },
    "requestPath": {
      "question-detector": "cvdigital/question-detector:0.2rc",
      "comprehension": "cvdigital/reading_comp:0.2rc",
      "kb-search": "cvdigital/kb_search:0.2rc"
    },
    "metrics": []
  },
  "strData": "aspirin and/or statins"
}
```

### Example Streamlit app

![katecheo](katecheo.gif)

We've also created an example [Streamlit app](https://www.streamlit.io/) to demonstrate Katecheo. Details on running the application are included [here](demo).

## Future extensions

In the future we intend to:

- Extend our knowledge base search methodology (e.g., to use bigrams and/or more sophisticated language models)
- Enable usage of a wider variety of pre-trained models (BERT, XLNet, etc.)
- Allow users to dynamically switch similarity thresholds and/or comprehension models

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
