from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import os
import urllib2

class KBSearch(object):
  SEARCH = 0
  TOPIC = 1

  available_topics = []
  recordsDict = {}
  recordsArray = []
  titles = []

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

    for topic in self.available_topics:
      filename = 'kb_' + topic + '.json'

      with open(filename) as json_file:  
        self.recordsArray = json.load(json_file)

        self.recordsDict = {}
        for element in self.recordsArray:
          self.recordsDict[element['title']] = element

        self.titles = self.recordsDict.keys()


  def downloadFile(self, url):
    filename = os.path.basename(url)
    fh = open(filename, "w")

    content = urllib2.urlopen(url)
    fh.write(content.read())

    fh.close()
    return


  def predict(self, X, features_names):
    response = {}

    if X[self.TOPIC] in self.available_topics:
        ret = process.extractOne(X[self.SEARCH], self.titles, scorer=fuzz.ratio)
        response = self.recordsDict[ret[0]]
    else:
      response = {
        "error": 'KBSearch/predict - Topic: ' + X[self.TOPIC] + ' not found'
      }

    return json.dumps(response)
