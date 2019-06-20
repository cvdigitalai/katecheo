from QuestionDetector import QuestionDetector

class QuestionDetectorModel(object):

  def __init__(self):
    self.model = QuestionDetector()

  def predict(self,X,features_names):
    """
    Return a prediction.

    Parameters
    ----------
    X : array-like
    feature_names : array of feature names (optional)
    """
    print("Predict called - will run identity function")
    text = X[0]
    return self.model.predict(text)
