import kb_answers
import json

class KBSearch(object):
    
    def __init__(self):
        # read in articles
        # read in title

    def predict(self,X,features_names):
        result = kb_answers.isQuestionAnswered(X[0])
        return json.dumps(result)
