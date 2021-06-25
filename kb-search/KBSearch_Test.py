"""
    python KBSearch_Test.py
"""
import json
import urllib.parse
import urllib.request
import unittest
import pprint
import sys
import os

os.environ[
    'KATECHEO_KB'] = 'faith=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_gq_6k_general.json,health=https://storage.googleapis.com/pachyderm-neuralbot/knowledge_bases/kb_wedmd_health.json'
os.environ['KATECHEO_ARTICLE_ID'] = 'article_url'
os.environ['KATECHEO_ARTICLE_TITLE_KEY'] = 'title'
os.environ['KATECHEO_ARTICLE_BODY_KEY'] = 'body'
os.environ['KATECHEO_SIMILARITY_THRESHOLD'] = '0.15'

pp = pprint.PrettyPrinter(indent=2)

class KBSearch_Test(unittest.TestCase):
    def test_topic_health(self):
        payload = {
            "params": "Can acupuncture help me loose weight?",
            "tags": {
                "question": True
            }
        }

        print('\x1b[31m' + str(payload) + '\x1b[0m')

        data = json.dumps(payload).encode('utf8')
        req = urllib.request.Request('http://localhost:6070/kbsearch', data, {'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req)

        data = json.load(resp)

        print("---- data: \n", data)

    def test_topic_faith(self):
        payload = {
            "params": "What about different Christian denominations?",
            "tags": {
                "question": True
            }
        }

        print('\x1b[31m' + str(payload) + '\x1b[0m')

        data = json.dumps(payload).encode('utf8')
        req = urllib.request.Request('http://localhost:6070/kbsearch', data, {'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req)

        data = json.load(resp)

        print("---- data: \n", data)


if __name__ == '__main__':
    unittest.main()


