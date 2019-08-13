"""
    python ReadingComp_Test.py
"""
import unittest
import json
import ReadingComp


class ReadingComp_Test(unittest.TestCase):
    def setUp(self):
        self.comprehension = ReadingComp.ReadingComp()

    def test_comprehension(self):
        params = ['Does some food increase pollen allergy symptoms?']

        response = self.comprehension.predict(params, "features",
                                              {'tags': {
                                                  'proceed': True
                                              }})
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
