from allennlp import pretrained

class ReadingComp(object):
    """
        ReadingComp takes as input the original input question plus the matched knowledge base article body text and
        uses a reading comprehension model to select an appropriate answer from within the kb article
    """
    def __init__(self):
        """
            During initialization, Allen's BiDAF model is setup
        """
        self.model = pretrained.bidirectional_attention_flow_seo_2017()

    def predict(self, X, feature_names, meta):
        """
            Given a long article body of text, returns a short sentence with the most pertinent phrases in sentence form 

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
        if 'tags' in meta and 'proceed' in meta['tags'] and meta['tags']['proceed']:
            if len(X) != 2:
                self.result = meta['tags']
                self.result['proceed'] = False
                self.result['point_of_failure'] = 'No Article Text'
                return ''
            prediction = self.model.predict(passage=str(X[0]),
                                            question=str(X[1]))['best_span_str']
            self.result = meta['tags']
            return prediction
        else:
            self.result = meta['tags']
            return ''

    def tags(self):
        return self.result
