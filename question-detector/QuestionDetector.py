from flask import Flask, request
import json
import requests

app = Flask(__name__)

class QuestionID:
    """
        QuestionID has the actual logic used to determine if sentence is a question
    """
    def padCharacter(self, character: str, sentence: str):
        if character in sentence:
            position = sentence.index(character)
            if position > 0 and position < len(sentence):

                # Check for existing white space before the special character.
                if (sentence[position - 1]) != " ":
                    sentence = sentence.replace(character, (" " + character))

        return sentence

    def predict(self, sentence: str):
        questionStarters = [
            "which", "wont", "cant", "isnt", "arent", "is", "do", "does",
            "will", "can"
        ]
        questionElements = [
            "who", "what", "when", "where", "why", "how", "sup", "?"
        ]

        sentence = sentence.lower()
        sentence = sentence.replace("\'", "")
        sentence = self.padCharacter('?', sentence)
        splitWords = sentence.split()

        if any(word == splitWords[0] for word in questionStarters) or any(
                word in splitWords for word in questionElements):
            return True
        else:
            return False

model = QuestionID()

@app.route('/questiondetector', methods=['POST'])
def detect_question():
    response = ""
    is_question = model.predict(request.json["params"])

    payload = {
        "params": request.json["params"],
        "meta": {
            "tags": {
                "question": is_question,
                "question_detector_error": "" if is_question else "This is not a question"
            }
        }
    }

    try:
        r = requests.post("http://kbsearch:6070/kbsearch", data=json.dumps(payload), headers={'content-type':'application/json'})
        response = r.text
    except requests.exceptions.RequestException as e:
        print(e)
        pass

    return response, 200

if __name__=='__main__':
    app.run('0.0.0.0', port=6060, debug=True )
    #serve(app, host='0.0.0.0', port=6080)
