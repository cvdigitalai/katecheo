from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import os
import urllib2

class KBSearch(object):
  SEARCH = 0
  TOPIC = 1

  available_topics = []

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


  def downloadFile(self, url):
    filename = os.path.basename(url)
    fh = open(filename, "w")

    content = urllib2.urlopen(url)
    fh.write(content.read())

    fh.close()
    return

  def predict(self, X, features_names):
    response = {'title': '12'}

    if X[self.TOPIC] in self.available_topics:
      filename = 'kb_' + X[self.TOPIC] + '.json'

      with open(filename) as json_file:  
        recordsArray = json.load(json_file)

        recordsDict = {}
        for element in recordsArray:
          recordsDict[element['title']] = element

        titles = []
        for index, rec in enumerate(recordsArray):
          titles.append(rec['title'])

        ret = process.extractOne(X[self.SEARCH], titles, scorer=fuzz.ratio)
        response = recordsDict[ret[0]]

    else:
      response = {
        "error": 'Topic: ' + X[self.TOPIC] + ' not found'
      }

    return json.dumps(response)
