class QuestionDetector(object):

  def __init__(self):
    self.model = QuestionID()

  def predict(self,X,features_names):
    """
    Return a prediction.

    Parameters
    ----------
    X : array-like
    feature_names : array of feature names (optional)
    """
    
    question = self.model.predict(X[0])
    self.result = {'proceed': question}
    if not question:
        self.result['point_of_failure'] = 'Not Question'

    return X

  def tags(self):
      return self.result

class QuestionID:

  def padCharacter(self, character: str, sentence: str):
    if character in sentence:
      position = sentence.index(character)
      if position > 0 and position < len(sentence):

        # Check for existing white space before the special character.
        if (sentence[position - 1]) != " ":
          sentence = sentence.replace(character, (" " + character))
    
    return sentence

  def predict(self, sentence: str):
    questionStarters = ["which", "wont", "cant", "isnt", "arent", "is", "do", "does", "will", "can", "is"]
    questionElements = ["who", "what", "when", "where", "why", "how", "sup", "?"]

    sentence = sentence.lower()
    sentence = sentence.replace("\'", "")
    sentence = self.padCharacter('?', sentence)
    splitWords = sentence.split()

    if any(word in splitWords[0] for word in questionStarters) or any(word in splitWords for word in questionElements):
      return True
    else:
      return False
