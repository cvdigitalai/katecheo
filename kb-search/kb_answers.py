import pymongo
import gq_search_plugin_adapter

MATCH_CONFIDENCE_THRESHOLD = 75

conn = pymongo.MongoClient('mongodb://app:IJggBGL2SmUl@34.239.210.203:27017/ice?authSource=user-data')
ice_db = conn["ice"]


def isAnswered(input, collection):
  return_this = []

  results = collection.find({})
  for result in results:
    confidence = gq_search_plugin_adapter.getMatch(result['article_title'], input)
    if confidence > MATCH_CONFIDENCE_THRESHOLD:
      return_this.append({
        'id': result['id'],
        'confidence': confidence,
        'article_title': result['article_title']
      })

  return return_this

def isQuestionAnswered(question):
  response = {}

  # First Pass
  results = isAnswered(question, ice_db['gq_answers_top_questions'])
  if results is not None and len(results):
    maxValue = results[0]['confidence']
    maxIndex = 0
    for index, result in enumerate(results):
      if result['confidence'] > maxValue:
        maxValue = result['confidence']
        maxIndex = index
    return results[maxIndex]

  # Second Pass
  results = isAnswered(question, ice_db['gq_answers_general'])
  if results is not None and len(results):
    maxValue = results[0]['confidence']
    maxIndex = 0
    for index, result in enumerate(results):
      if result['confidence'] > maxValue:
        maxValue = result['confidence']
        maxIndex = index
    response = results[maxIndex]

  return response
