from allennlp import pretrained

class ReadingComp(object):
    def __init__(self):
        self.model = pretrained.bidirectional_attention_flow_seo_2017() 

    def predict(self, X, feature_names, meta):

        # logic from parent
        if 'tags' in meta and 'proceed' in meta['tags'] and meta['tags']['proceed']:
            prediction = self.model.predict(passage=str(X[0]), question=str(X[1]))['best_span_str']
            self.result = meta['tags']
            return prediction
        else:
            self.result = meta['tags']
            return ''

    def tags(self):
      return self.result

