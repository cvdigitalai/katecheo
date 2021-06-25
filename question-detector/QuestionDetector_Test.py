"""
    python QuestionDetector_Test.py
"""
import unittest
import json

import requests

import json
import pprint

import unittest

pp = pprint.PrettyPrinter(indent=2)


class QuestionDetector_Test(unittest.TestCase):
    def test_question(self):
        
        payload = {
            "params": "Can acupuncture help me loose weight?"
        }
        
        print('\x1b[31m' + payload['params'] + '\x1b[0m')

        try:
            r = requests.post("http://localhost:6080/questiondetector", data=json.dumps(payload), headers={'content-type':'application/json'}) 
            
        except requests.exceptions.RequestException as e:
            print(e)
            pass

    def test_non_question(self):
        
        payload = {
            "params": "God is good."
        }
        
        print('\x1b[31m' + payload['params'] + '\x1b[0m')

        try:
            resp = requests.post("http://localhost:6080/questiondetector", data=json.dumps(payload), headers={'content-type':'application/json'}) 
            
        except requests.exceptions.RequestException as e:
            print(e)
            pass

if __name__ == '__main__':
    unittest.main()