"""
    python KBSearch_Test.py
"""
import unittest
import json
import os
os.environ[
    'KATECHEO_KB'] = 'faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_faith.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json'

import KBSearch


class KBSearch_Test(unittest.TestCase):
    def setUp(self):
        self.search = KBSearch.KBSearch()

    def test_topic_health(self):
        params = ['Does some food increase pollen allergy symptoms?', 'health']

        response = self.search.predict(params, "features")
        self.assertIsNotNone(response)
        obj = json.loads(response)
        if 'error' in obj:
            self.assertTrue(False, obj)

    def test_topic_faith(self):
        params = ['Life Belt or Lifeboat', 'faith']

        response = self.search.predict(params, "features")
        self.assertIsNotNone(response)
        obj = json.loads(response)
        if 'error' in obj:
            self.assertTrue(False, obj)

if __name__ == '__main__':
    unittest.main()