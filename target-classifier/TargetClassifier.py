import zipfile
import urllib

import spacy

class TargetClassifier(object):
    def __init__(self):

        # TODO - pull model from GCS with authenticated client
        # Download the model
        u = "https://storage.googleapis.com/pachyderm-neuralbot/model-2.1.4.zip"
        urllib.request.urlretrieve(u, "model.zip")
        zip_ref = zipfile.ZipFile("model.zip", 'r')
        zip_ref.extractall(".")
        zip_ref.close()

        # Load the trained NER model
        self.nlp = spacy.load("evangelism_model")

    def predict(self,X,feature_names):

        prediction = False

        # Get the result from the NER model for each question.
        doc = self.nlp(str(X[0]))

        # Check if the model has recognised the trained entities in the question.
        if doc.ents:
            prediction = True

        return str(prediction)
