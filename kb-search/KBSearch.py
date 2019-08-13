from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import numpy as np
import os
import urllib.request
import numpy as np


class KBSearch(object):
    """
    KBSearch searches for a phrase in the list of knowledge base articles' title field. It uses FuzzyWuzzy for matching

    The knowledge base articles list is in JSON list format and stored in the cloud
    """
    SEARCH_PHRASE = 0
    TOPIC = 1

    availableKB = []
    records = {}
    titles = {}
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

        # For each topic
        #   - create a list of titles
        #   - create a list of titles and article bodies
        self.records = {}
        self.titles = {}
        for kb in self.availableKB:
            with open(os.path.basename(kb['url'])) as json_file:
                parsed = json.load(json_file)

                self.records[kb['topic']] = {}

                for element in parsed:
                    self.records[kb['topic']][element['title']] = element

                self.titles[kb['topic']] = list(
                    self.records[kb['topic']].keys())

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
        response = {}

        # Logic from parent
        if 'tags' in meta and 'proceed' in meta['tags'] and meta['tags'][
                'proceed']:
            try:
                # Try matching each record's title field with search phrase
                didNotMatchAvailableTopics = True
                for kb in self.availableKB:
                    if meta['tags']['topic'] == kb['topic']:
                        didNotMatchAvailableTopics = False
                        ret = process.extractOne(
                            X[self.SEARCH_PHRASE],
                            self.titles[meta['tags']['topic']],
                            scorer=fuzz.ratio)
                        X = np.append([
                            self.records[meta['tags']['topic']][ret[0]]['body']
                        ], X)
                        self.result = meta['tags']
                        return X

                # Notify caller that something went wrong
                if didNotMatchAvailableTopics:
                    self.result = meta['tags']
                    self.result['proceed'] = False
                    self.result['point_of_failure'] = 'KB for topic \"' + meta[
                        'tags']['topic'] + '\" not found'
                    return X

            except KeyError:
                self.result = meta['tags']
                self.result['proceed'] = False
                self.result['point_of_failure'] = 'KB key error'
                return X

        else:
            self.result = meta['tags']
            return X

    def tags(self):
        return self.result
