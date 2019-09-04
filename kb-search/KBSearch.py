from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import json
import numpy as np
import os
import urllib.request


class KBSearch(object):
    """
    KBSearch searches for a phrase in the list of knowledge base articles' title field. It uses FuzzyWuzzy for matching

    The knowledge base articles list is in JSON list format and stored in the cloud
    """
    vectorizer = {}
    allDocs = {}
    allVector = {}
    corpus = {}
    availableKB = []
    result = {}

    def __init__(self):
        """
        During initialization:
        
        - titles for each topic are read from 'knowledge base list' and stored in 'records' with this format:

            records['health']['health_article1'] = {'title': 'health_article1', 'body': '---'}
                            ['health_article2'] = {'title': 'health_article2', 'body': '---'}
                            ['health_article3'] = {'title': 'health_article3', 'body': '---'}
                            ...
                            ['health_articleN'] = {'title': 'health_articleN', 'body': '---'}

            records['faith']['faith_article1'] = {'title': 'faith_article1', 'body': '---'}
                            ['faith_article2'] = {'title': 'faith_article2', 'body': '---'}
                            ['faith_article3'] = {'title': 'faith_article3', 'body': '---'}
                            ...
                            ['faith_articleN'] = {'title': 'faith_articleN', 'body': '---'}

            Note that in "records['health']['health_article1']", the title 'health_article1' is also the key to that element in the list


        - Another list of just the titles is stored in this format:

            titles = ['title1', 'title2', ... 'titleN']


        - The configuration variable KATECHEO_KB comes from the environment and it would typically look like this:
            'health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json,faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json'

            The above example has two topics: 'health' and 'faith'. Each element in the list also has a URL to the corresponding knowledge base list
        """

        # Parse through KATECHEO_KB to get topic and associated knowledge base file
        kb_list = os.environ['KATECHEO_KB'].split(',')
        self.availableKB = []
        for kb_file in kb_list:
            parts = kb_file.split('=')
            self.availableKB.append({'topic': parts[0], 'url': parts[1]})
            self.downloadFile(parts[1])

        for kb in self.availableKB:
            with open(os.path.basename(kb['url'])) as json_file:
                self.corpus[kb['topic']] = json.load(json_file)

                self.allDocs[kb['topic']] = []

                for doc in self.corpus[kb['topic']]:
                    self.allDocs[kb['topic']].append(
                        str(doc['title']) + " " + str(doc['body']))

                self.vectorizer[kb['topic']] = TfidfVectorizer(
                    ngram_range=(1, 2))  #
                self.allVector[kb['topic']] = self.vectorizer[
                    kb['topic']].fit_transform(self.allDocs[kb['topic']])

    def downloadFile(self, url):
        """
        Helper function to download knowledge base files
        """
        urllib.request.urlretrieve(url, os.path.basename(url))
        return

    def predict(self, X, features_names, meta):
        """
        Searches for a phrase in topic's knowledge base list using FuzzyWuzzy matching

        Parameters
        ----------
        X[0]
            The phrase to be searched
        X[1]
            The topic in which the search has to be made

        Returns
        -------
        response:
            The element in knowledge base list which matched the search phrase
        """

        question = ""

        # Logic from parent
        if 'tags' in meta and 'topic' in meta['tags']:
            didNotMatchAvailableTopics = True
            for kb in self.availableKB:
                if meta['tags']['topic'] == kb['topic']:
                    didNotMatchAvailableTopics = False
                    question = X[0]

                    questionVector = self.vectorizer[kb['topic']].fit(
                        self.allDocs[kb['topic']])
                    questionVector = questionVector.transform([question])

                    # Cosine Similarity
                    cosineSimilarity = cosine_similarity(
                        self.allVector[kb['topic']], questionVector).flatten()

                    foundFlag = False
                    maxIndex = 0
                    maxCos = 0

                    for index, doc in enumerate(self.corpus[kb['topic']], 0):
                        doc['cos_value'] = cosineSimilarity[index]

                    for index, doc in enumerate(self.corpus[kb['topic']], 0):
                        if cosineSimilarity[index] > maxCos:
                            foundFlag = True
                            maxCos = cosineSimilarity[index]
                            maxIndex = index

                    if foundFlag:
                        article_source = ""
                        if "article_url" in self.corpus[kb['topic']][maxIndex]:
                            article_source = str(self.corpus[kb['topic']]
                                                 [maxIndex]['article_url'])
                        else:
                            article_source = str(
                                self.corpus[kb['topic']][maxIndex]['body'])

                        X = np.append(
                            [str(self.corpus[kb['topic']][maxIndex]['body'])],
                            X)

                        self.result = meta['tags']
                        self.result["kb_article"] = True
                        self.result["article_source"] = article_source
                        return X

            # Notify caller that something went wrong
            if didNotMatchAvailableTopics:
                self.result = meta['tags']
                self.result['kb_search_error'] = 'KB for topic \"' + meta[
                    'tags']['topic'] + '\" not found'
                return X

            self.result = meta['tags']
            self.result[
                'kb_search_error'] = 'Could not match "' + question + '" with any article on the topic of "' + meta[
                    'tags']['topic'] + '"'
            return X

        self.result = meta['tags']
        return X

    def tags(self):
        return self.result
