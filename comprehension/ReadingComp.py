from flask import Flask, request, jsonify
import os


import torch
from transformers import pipeline
import numpy as np
# from allennlp import pretrained

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

        # if os.environ.get('KATECHEO_COMP_MODEL') is not None:
        #     if os.environ.get('KATECHEO_COMP_MODEL').lower() == 'bidaf':
        #         self.model = pretrained.bidirectional_attention_flow_seo_2017()
        #         self.bidaf = True
        #     else:
        #         self.model = pipeline('question-answering')
        # else:
        #     self.model = pipeline('question-answering')

    def predict(self, X, feature_names, meta):
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
        if 'tags' in meta and 'on_topic' in meta['tags'] and meta['tags']['on_topic'] == True:
            if len(X) != 2:
                self.result = meta['tags']
                self.result['comprehension_error'] = 'No Article Text'
                return ''
            
            if self.bidaf:
                prediction = self.model.predict(passage=str(X[0]),
                                            question=str(X[1]))['best_span_str']
                
            else:
                prediction = self.model({'question': str(X[1]), 'context': str(X[0])})['answer']
            
           
            self.result = meta['tags']
            self.result['comprehension_error'] = ''
            if self.bidaf:
                self.result['comprehension_model'] = 'BiDAF'
            else:
                self.result['comprehension_model'] = 'BERT'
            
            #print("Prediction: ", prediction)
            return prediction

        self.result = meta['tags']
        return self.result

    

app = Flask(__name__)

obj = ReadingComp()



@app.route('/comprehension', methods=['POST'])
def read_comprehension():
    inbound = request.json

    #X = np.array([inbound['params']])
    X = inbound['params']
    meta = {
        "tags": {
            "question": inbound['tags']['question'],
            'on_topic': inbound['tags']['on_topic']
        }
    }
   
    retval = obj.predict(X, None, meta)
    print("\n retval from ReadingComp: \n", retval, "\n")
    print("\n Type of retval from ReadingComp:\n", type(retval), "\n")

    resp_obj = {}
    resp_obj["data"] = retval
    resp_obj["question"] = inbound['tags']['question']
    resp_obj["question"] = inbound['tags']['on_topic']

    return jsonify(resp_obj)

if __name__ == "__main__":
    app.run('0.0.0.0', port=6080, debug=True) 
