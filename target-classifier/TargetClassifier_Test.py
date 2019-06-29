"""
    python QuestionDetector_Test.py
"""
import unittest
import json
import os
os.environ[
    'KATECHEO_NER'] = 'health=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/health.zip,faith=https://storage.googleapis.com/pachyderm-neuralbot/ner_models/faith.zip'
import TargetClassifier


class TargetClassifier_Test(unittest.TestCase):
    def setUp(self):
        self.classifier = TargetClassifier.TargetClassifier()

    def test_get_topic(self):
        params = ['Does some food increase pollen allergy symptoms?']

        response = self.classifier.predict(params, "features", {'tags': {'proceed': True}})
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()