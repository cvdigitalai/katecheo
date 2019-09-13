"""
    python KBSearch_Test.py
"""
import unittest
import json
import os
os.environ[
    'KATECHEO_KB'] = 'faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_health.json'
import KBSearch


class KBSearch_Test(unittest.TestCase):
    def setUp(self):
        self.search = KBSearch.KBSearch()

    def test_topic_health(self):
        params = ['Does some food increase pollen allergy symptoms?', 'health']

        response = self.search.predict(
            params, "features", {'tags': {
                'proceed': True,
                "topic": "health"
            }})
        print("health response", response)
        self.assertIsNotNone(response)

    def test_topic_faith(self):
        params = ['Is Christianity a true religion?', 'faith']

        response = self.search.predict(
            params, "features", {'tags': {
                'proceed': True,
                "topic": "faith"
            }})
        print("faith response", response)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
