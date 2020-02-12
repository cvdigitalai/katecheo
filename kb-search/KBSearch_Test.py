"""
    python KBSearch_Test.py
"""
import unittest
import json
import os

import KBSearch

os.environ[
    'KATECHEO_KB'] = 'faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json'
os.environ['KATECHEO_ARTICLE_ID'] = 'article_url'
os.environ['KATECHEO_ARTICLE_TITLE_KEY'] = 'title'
os.environ['KATECHEO_ARTICLE_BODY_KEY'] = 'body'
os.environ['KATECHEO_SIMILARITY_THRESHOLD'] = '0.19'


class KBSearch_Test(unittest.TestCase):
    def setUp(self):
        self.search = KBSearch.KBSearch()

    def test_topic_health(self):
        params = ['Can acupuncture help me loose weight?']

        response = self.search.predict(params, "features",
                                       {'tags': {
                                           'question': True
                                       }})
        print("health response", response)
        self.assertIsNotNone(response)

    def test_topic_faith(self):
        params = ['What about different Christian denominations?']

        response = self.search.predict(params, "features",
                                       {'tags': {
                                           'question': True
                                       }})
        print("faith response", response)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
