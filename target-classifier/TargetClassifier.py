import zipfile
import urllib
import os
import spacy


class TargetClassifier(object):
    def __init__(self):
        """
            During initialization, spaCy models are loaded and kept ready for classifying a sentence to a topic
        """

        modelInfoFromEnv = os.environ['KATECHEO_NER']
        '''
            Parse the String in the environment variable.
            - Each model information is separated by ','
            - A specific model name and it's NER model location URL is separated by '='
        '''
        modelInfos = [
            sentence.split('=') for sentence in modelInfoFromEnv.split(',')
        ]

        nlpModels = {}

        # Iterate through each entry with the model information.
        for modelInfo in modelInfos:
            modelName = modelInfo[0]
            modelURL = modelInfo[1]

            # Download the model
            modelRootDirectory = "./" + modelName

            # Check if the model files already exists.
            if (modelName not in os.listdir(".")):
                urllib.request.urlretrieve(modelURL, modelName + ".zip")
                zipRef = zipfile.ZipFile(modelName + ".zip", 'r')
                zipRef.extractall(modelRootDirectory)
                zipRef.close()

            # Get the internal directory of the NER model.
            modelMainDirectory = os.listdir('./' + modelName)[0]

            # Check if the model directory has been downloaded.
            if (modelMainDirectory):

                # Load the spaCy models.
                nlpModels[modelName] = spacy.load(
                    os.path.join(modelRootDirectory, modelMainDirectory))

        self.models = nlpModels

    """
        Returns a string with data passed on from the previous models.

        Parameters
        ----------
        X : list of input texts
        feature_names : list of feature names
        meta : object with additional tags
    """
    def predict(self, X, feature_names, meta):

        # logic from parent
        if 'tags' in meta and 'question' in meta['tags'] and meta['tags'][
                'question']:

            topicName = ""
            matchedEntities = []

            # Get the text string that is to be classified.
            messageText = str(X[0])

            # Iterate through all the models
            for topic, model in self.models.items():

                # Get the inference result from the NER model for a question.
                doc = model(messageText)

                # Check if the model has recognised the trained entities in the question.
                if doc.ents:
                    topicName = topic
                    matchedEntities.append(doc.ents)

            # TODO: List out all the topics with a percentage of the match confidence.
            # Currently we would like to return classification result
            # only if it matches a single topic.
            if len(matchedEntities) == 1:
                self.result['topic'] = topicName
                return X
            else:
                self.result['topic_classifier_error'] = 'No Matching Topic'
                return X

        else:
            self.result = meta['tags']
            return X

    def tags(self):
        return self.result
