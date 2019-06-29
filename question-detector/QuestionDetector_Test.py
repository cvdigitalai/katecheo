"""
    python QuestionDetector_Test.py
"""
import unittest
import json
import QuestionDetector


class QuestionDetector_Test(unittest.TestCase):
    def setUp(self):
        self.question = QuestionDetector.QuestionDetector()

    def test_topic_health(self):
        params = ['Does some food increase pollen allergy symptoms?']

        response = self.question.predict(params, "features")
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()