import zipfile
import urllib
import os
import spacy


class TargetClassifier(object):
    """
    TargetClassifier attempts to classify the input question into one of the topics
    """
    models = {}

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

        self.models = {}

        # Iterate through each entry with the model information.
        for modelInfo in modelInfos:
            modelName = modelInfo[0]
            modelURL = modelInfo[1]

            # Download the model
            modelRootDirectory = "./" + modelName

            # Check if the model files already exists.
            if modelName not in os.listdir("."):
                urllib.request.urlretrieve(modelURL, modelName + ".zip")
                zipRef = zipfile.ZipFile(modelName + ".zip", 'r')
                zipRef.extractall(modelRootDirectory)
                zipRef.close()

            # Get the internal directory of the NER model.
            modelMainDirectory = os.listdir('./' + modelName)[0]

            # Check if the model directory has been downloaded.
            if modelMainDirectory:

                # Load the spaCy models.
                self.models[modelName] = spacy.load(
                    os.path.join(modelRootDirectory, modelMainDirectory))


    def predict(self, X, feature_names, meta):
        """
        Returns the search string and topic to which it was classified

        Parameters
        ----------
        X : array-like
        feature_names : array of feature names (optional)
        """

        # logic from parent
        if 'tags' in meta and 'proceed' in meta['tags'] and meta['tags']['proceed']:

            topicName = ""
            matchedEntities = []

            # Get the text string that is to be classified.
            messageText = str(X[0])

            # Iterate through all the models
            """
            TODO: 'model' is causing a crash. Needs fix ASAP.
            I'm blocking the offending part of the code to get other things done like code formatting, comments, tests, etc
            ---
                        ======================================================================
                        ERROR: test_get_topic (__main__.TargetClassifier_Test)
                        ----------------------------------------------------------------------
                        Traceback (most recent call last):
                        File "TargetClassifier_Test.py", line 19, in test_get_topic
                            response = self.classifier.predict(params, "features", {'tags': {'proceed': True}})
                        File "/Users/shirish/workarea/katecheo/target-classifier/TargetClassifier.py", line 83, in predict
                            doc = model(messageText)
                        File "/anaconda3/lib/python3.7/site-packages/spacy/language.py", line 390, in __call__
                            doc = proc(doc, **component_cfg.get(name, {}))
                        File "nn_parser.pyx", line 205, in spacy.syntax.nn_parser.Parser.__call__
                        File "nn_parser.pyx", line 244, in spacy.syntax.nn_parser.Parser.predict
                        File "nn_parser.pyx", line 257, in spacy.syntax.nn_parser.Parser.greedy_parse
                        File "/anaconda3/lib/python3.7/site-packages/thinc/neural/_classes/model.py", line 165, in __call__
                            return self.predict(x)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/neural/_classes/model.py", line 129, in predict
                            y, _ = self.begin_update(X, drop=None)
                        File "_parser_model.pyx", line 214, in spacy.syntax._parser_model.ParserModel.begin_update
                        File "_parser_model.pyx", line 262, in spacy.syntax._parser_model.ParserStepModel.__init__
                        File "/anaconda3/lib/python3.7/site-packages/thinc/neural/_classes/feed_forward.py", line 46, in begin_update
                            X, inc_layer_grad = layer.begin_update(X, drop=drop)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 264, in begin_update
                            X, bp_layer = layer.begin_update(layer.ops.flatten(seqs_in, pad=pad), drop=drop)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/neural/_classes/feed_forward.py", line 46, in begin_update
                            X, inc_layer_grad = layer.begin_update(X, drop=drop)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 348, in uniqued_fwd
                            Y_uniq, bp_Y_uniq = layer.begin_update(X_uniq, drop=drop)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/neural/_classes/feed_forward.py", line 46, in begin_update
                            X, inc_layer_grad = layer.begin_update(X, drop=drop)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in begin_update
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in <listcomp>
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 225, in wrap
                            output = func(*args, **kwargs)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in begin_update
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in <listcomp>
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 225, in wrap
                            output = func(*args, **kwargs)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in begin_update
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in <listcomp>
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 225, in wrap
                            output = func(*args, **kwargs)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in begin_update
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 132, in <listcomp>
                            values = [fwd(X, *a, **k) for fwd in forward]
                        File "/anaconda3/lib/python3.7/site-packages/thinc/api.py", line 225, in wrap
                            output = func(*args, **kwargs)
                        File "/anaconda3/lib/python3.7/site-packages/thinc/neural/_classes/static_vectors.py", line 73, in begin_update
                            dotted = self.ops.gemm(vectors, self.W, trans2=True)
                        File "ops.pyx", line 404, in thinc.neural.ops.NumpyOps.gemm
                        ValueError: Buffer and memoryview are not contiguous in the same dimension.
            ---
            for topic, model in self.models.items():

                # Get the inference result from the NER model for a question.
                doc = model(messageText)

                # Check if the model has recognised the trained entities in the question.
                if doc.ents:
                    topicName = topic
                    matchedEntities.append(doc.ents)
            """

            # TODO: List out all the topics with a percentage of the match confidence.
            # Currently we would like to return classification result
            # only if it matches a single topic.
            if len(matchedEntities) == 1:
                self.result = {'proceed': True}
                self.result['topic'] = topicName
                return X
            else:
                self.result = {'proceed': False}
                self.result['point_of_failure'] = 'No Matching Topic'
                return X

        else:
            self.result = meta['tags']
            return X

    def tags(self):
        return self.result
