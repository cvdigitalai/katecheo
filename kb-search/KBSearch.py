from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import os
import urllib.request
import numpy as np

class KBSearch(object):
  SEARCH = 0
  TOPIC = 1

  available_topics = []
  recordsDict = {}
  recordsArray = []
  titles = {}

  def __init__(self):
    # This is format of injected env var
    # 'faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json'

    # first split by 'comma' to get topics
    kb_list = os.environ['KATECHEO_KB'].split(',')
    for kb_file in kb_list:
      # next split each by 'equals' to get the RHS (path to json)
      parts = kb_file.split('=')
      self.available_topics.append(parts[0])
      self.downloadFile(parts[1])

    self.recordsDict = {}
    for topic in self.available_topics:
      filename = 'kb_' + topic + '.json'

      with open(filename) as json_file:
        self.recordsArray = json.load(json_file)

        self.recordsDict[topic] = {}
        for element in self.recordsArray:
          self.recordsDict[topic][element['title']] = element

        self.titles[topic] = list(self.recordsDict[topic].keys())


  def downloadFile(self, url):
    filename = os.path.basename(url)
    urllib.request.urlretrieve(url, filename)
    return

  def predict(self, X, features_names, meta):

    # logic from parent
    if 'tags' in meta and 'proceed' in meta['tags'] and meta['tags']['proceed']:

        try:
            if meta['tags']['topic'] in self.available_topics:
                ret = process.extractOne(X[self.SEARCH], self.titles[meta['tags']['topic']], scorer=fuzz.ratio)
                X = np.append([self.recordsDict[meta['tags']['topic']][ret[0]]['body']], X)
                self.result = meta['tags']
                return X
            else:
                self.result = meta['tags']
                self.result['proceed'] = False
                self.result['point_of_failure'] = 'KB for topic \"' + meta['tags']['topic'] + '\" not found'
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
