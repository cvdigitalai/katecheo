from flask import Flask, request, jsonify
import os
import torch
from transformers import pipeline
import numpy as np

app = Flask(__name__)

class ReadingComp(object):
    """
        ReadingComp takes as input the original input question plus the matched knowledge base article body text and
        uses a reading comprehension model to select an appropriate answer from within the kb article.
    """

    def __init__(self):
        """
            During initialization, setup Hugging Face's BERT Implementation (by default), or AllenNLP's implementation
            of BiDAF if specified via environmental variable.
        """
        self.model = pipeline('question-answering')
        self.bidaf = False

    def predict(self, X, feature_names, package):
        """
            Given a long article body of text, returns a span that answers the provided question.

            Parameters
            ----------
            X[0]
                The text which needs to be reduced by comprehension

            Returns
            -------
            response:
                The reduced text
        """
        # logic from parent
        if package and 'meta' in package and 'tags' in package['meta'] and 'on_topic' in package['meta']['tags'] and package['meta']['tags']['on_topic'] == True:
            if len(X) != 2:
                package['meta']['tags']['comprehension_error'] = 'No Article Text'
                return package

            if self.bidaf:
                prediction = self.model.predict(passage=str(X[0]),
                                            question=str(X[1]))['best_span_str']
            else:
                prediction = self.model({'question': str(X[1]), 'context': str(X[0])})['answer']

            package['meta']['tags']['comprehension_error'] = ''
            if self.bidaf:
                package['meta']['tags']['comprehension_model'] = 'BiDAF'
            else:
                package['meta']['tags']['comprehension_model'] = 'BERT'

            package['strData'] = prediction
            return package

        package['meta']['tags']['comprehension_error'] = 'Not enough meta data to proceed'
        return package

obj = ReadingComp()

@app.route('/comprehension', methods=['POST'])
def read_comprehension():
    X = request.json['params']
    package = {
        "meta": request.json["meta"]
    }

    retval = obj.predict(X, None, package)

    return jsonify(retval)

if __name__ == "__main__":
    app.run('0.0.0.0', port=6080, debug=True)
