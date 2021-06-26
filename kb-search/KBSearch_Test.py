"""
    python KBSearch_Test.py
"""
import json
import urllib.request
import unittest
import pprint
import requests

class KBSearch_Test(unittest.TestCase):
    def test_topic_health(self):
        payload = {
            "params": "Can acupuncture help me loose weight?",
            "meta": {
                "tags": {
                    "question": True
                }
            }
        }

        print('\x1b[31m' + str(payload) + '\x1b[0m')
        try:
            r = requests.post("http://localhost:6070/kbsearch", data=json.dumps(payload), headers={'content-type':'application/json'})
            print("Response Text: ", r.text)

        except requests.exceptions.RequestException as e:
            print(e)
            pass

    def test_topic_faith(self):
        payload = {
            "params": "What about different Christian denominations?",
            "meta": {
                "tags": {
                    "question": True
                }
            }
        }

        print('\x1b[31m' + str(payload) + '\x1b[0m')

        try:
            r = requests.post("http://localhost:6070/kbsearch", data=json.dumps(payload), headers={'content-type':'application/json'})
            print("Response Text: ", r.text)

        except requests.exceptions.RequestException as e:
            print(e)
            pass

if __name__ == '__main__':
    unittest.main()
