import os

import torch
from transformers import *
from allennlp import pretrained

class ReadingComp(object):
    """
        ReadingComp takes as input the original input question plus the matched knowledge base article body text and
        uses a reading comprehension model to select an appropriate answer from within the kb article.
    """

    def __init__(self):
        """
            During initialization, setup Hugging Face's DistilBERT (by default), or AllenNLP's implementation
            of BiDAF if specified via environmental variable.
        """

        self.bidaf = False

        if os.environ.get('KATECHEO_COMP') is not None:
            if os.environ.get('KATECHEO_COMP').lower() == 'bidaf':
                self.model = pretrained.bidirectional_attention_flow_seo_2017()
                self.bidaf = True
            else:
                self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                self.model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
        else:
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')

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
        if 'tags' in meta and 'kb_article' in meta['tags'] and meta['tags']['kb_article'] == True:
            if len(X) != 2:
                self.result = meta['tags']
                self.result['comprehension_error'] = 'No Article Text'
                return ''

            if self.bidaf:
                prediction = self.model.predict(passage=str(X[0]),
                                            question=str(X[1]))['best_span_str']
            else:
                indexed_tokens = self.tokenizer.encode(str(X[0]), str(X[1]), add_special_tokens=True)
                tokens_tensor = torch.tensor([indexed_tokens])
                start_logits, end_logits = self.model(tokens_tensor)
                prediction = self.tokenizer.decode(indexed_tokens[torch.argmax(start_logits):torch.argmax(end_logits)+1])
            
            self.result = meta['tags']
            self.result['comprehension_error'] = ''
            return prediction

        self.result = meta['tags']
        return X

    def tags(self):
        return self.result
