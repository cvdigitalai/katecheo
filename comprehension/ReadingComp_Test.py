"""
    python ReadingComp_Test.py
"""
import unittest
import json
import requests

class ReadingComp_Test(unittest.TestCase):
    def test_comprehension(self):
        payload = {
            "params" : [
            'Jesus of Nazareth, also known as Jesus Christ, was a Jewish teacher and reformer of religion who has become the main and central figure of Christianity. Christians follow the example of Jesus, accept his words to be true, and worship him as God. He is one of the most famous, most recognized, and most influential persons in the world history',
            'Who is Jesus?'
            ],
            "meta": {
                "tags": {
                    "question": True,
                    "on_topic": True,
                    "topic": "health"
                }
            }
        }

        print('\x1b[31m' + str(payload['params']) + '\x1b[0m')

        try:
            r = requests.post("http://localhost:6080/comprehension", data=json.dumps(payload), headers={'content-type':'application/json'})
            rdict = json.loads(r.text)
            print("Response: ", str(rdict))

        except requests.exceptions.RequestException as e:
            print(e)
            pass

if __name__ == '__main__':
    unittest.main()
