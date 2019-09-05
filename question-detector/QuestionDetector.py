class QuestionDetector(object):
    """
        QuestionDetector determines if the input text is actually a question
    """
    result = {}

    def __init__(self):
        """
            During initialization, QuestionID is set as the model
        """
        self.model = QuestionID()

    def predict(self, X, features_names):
        """
            Returns a prediction

            Parameters
            ----------
            X : array-like
            feature_names : array of feature names (optional)
        """
        question = self.model.predict(X[0])
        if question:
            self.result['question'] = True
            self.result['question_detector_error'] = ''
        else:
            self.result['question'] = False
            self.result['question_detector_error'] = 'Not Question'

        return X

    def tags(self):
        return self.result


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
            "will", "can", "is"
        ]
        questionElements = [
            "who", "what", "when", "where", "why", "how", "sup", "?"
        ]

        sentence = sentence.lower()
        sentence = sentence.replace("\'", "")
        sentence = self.padCharacter('?', sentence)
        splitWords = sentence.split()

        if any(word in splitWords[0] for word in questionStarters) or any(
                word in splitWords for word in questionElements):
            return True
        else:
            return False
