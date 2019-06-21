import json
import os
os.environ['KATECHEO_KB'] = 'faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json'

import KBSearch

search = KBSearch.KBSearch()

params = [
  'Why are the estimates of obesity prevalence in England wildly different?',
  'health'
]

response = search.predict(params, "features")
obj = json.loads(response)
if response:
  print('Found this TITLE: ' + obj['title'] + ', BODY' + obj['body'])
else:
  print('Not found')
