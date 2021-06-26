from flask import Flask, Response, jsonify, request
import copy
import json
import nltk
import numpy as np
import os
import re
import requests
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)
tfidf_vectorizer = None
vectorized_knowledge_base = None
common_knowledge_base = []
common_knowledge_base_clean = []
result = {}

class KBSearch(object):
    """
    KBSearch searches uses 'cosine similarity' to measure the similarity between
    a given phrase and an article from a knowledge base.
    """
    tfidf_vectorizer = None
    vectorized_knowledge_base = None
    common_knowledge_base = []
    common_knowledge_base_clean = []
    result = {}

    def __init__(self):
        '''
            Parse through the environment variable 'KATECHEO_KB' string.
            - Each knowledge base and it's information is separated by ','
            - A specific topic and it's knowledge base URL is separated by '='
            Create an object which holds the information of the knowledge bases in the
            format shown below:
            {
                "topic_1": "knowledge_base_1_url",
                "topic_2": "knowledge_base_2_url",
                ...
            }
        '''
        kb_info = [
            sentence.split('=')
            for sentence in os.environ['KATECHEO_KB'].split(',')
        ]

        knowledge_bases_raw_data = {}

        # Iterate through the different knowledge bases.
        for kb in kb_info:
            topic = kb[0]
            kb_url = kb[1]

            # Download the knowledge base files.
            try:
                r = requests.get(kb_url, allow_redirects=True)
                open("/kb_data/" + os.path.basename(kb_url), 'wb').write(r.content)
            except requests.exceptions.RequestException as e:
                print("Error in downloading KB URL")
                print(e)
                return

            # Load the downloaded JSON files.
            with open("/kb_data/" + os.path.basename(kb_url)) as f:
                knowledge_bases_raw_data[topic] = json.load(f)

        # Iterate through each article from each topic and get only the
        # article ID, title and body of each article.
        for topic in knowledge_bases_raw_data:
            for article in knowledge_bases_raw_data[topic]:
                if os.environ['KATECHEO_ARTICLE_ID'] and os.environ[
                        'KATECHEO_ARTICLE_TITLE_KEY'] and os.environ['KATECHEO_ARTICLE_BODY_KEY']:
                    self.common_knowledge_base.append({
                        os.environ['KATECHEO_ARTICLE_ID']:
                        article[os.environ['KATECHEO_ARTICLE_ID']],
                        "content":
                        article[os.environ['KATECHEO_ARTICLE_TITLE_KEY']] + " " +
                        article[os.environ['KATECHEO_ARTICLE_BODY_KEY']],
                        "topic":
                        topic
                    })

        # The 'copy.deepcopy()' method helps in copying the value of variable rather
        # than creating a reference which is what python does by default.
        self.common_knowledge_base_clean = copy.deepcopy(
            self.common_knowledge_base)

        # Clean-up the content of the articles.
        for article in self.common_knowledge_base_clean:
            article["content"] = self.clean_text_and_remove_stopwords(
                article["content"])

        # Create a Bag of Word for the "combined (topic1 + topic2 + ...)" data using TF-IDF
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        kb_content = [
            doc['content'] for doc in self.common_knowledge_base_clean
        ]
        self.tfidf_vectorizer.fit(kb_content)
        self.knowledge_base_vectorized = self.tfidf_vectorizer.transform(
            kb_content)

    def clean_text_and_remove_stopwords(self, text):
        # Remove punctuations
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

        # Remove unnecessary white space.
        text = re.sub(r'\s+', ' ', text).strip()

        # Convert every word to lowercase.
        text = text.lower()

        # Tokenize each word and remove common stop words in English.
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_tokens = [w for w in word_tokens if not w in stop_words]
        text = " ".join(filtered_tokens)

        return text

    def get_matching_article(self, corpus, cos_similarity):
        max_cosine_similarity = 0
        article_index = 0

        for index, _ in enumerate(corpus):

            # Get the article from the combined knowledge base with the highest
            # cosine similarity to the question.
            if cos_similarity[index] > max_cosine_similarity:
                max_cosine_similarity = cos_similarity[index]
                article_index = index

        return article_index, max_cosine_similarity

    def predict(self, X, feature_names, package):
        if package and 'meta' in package and 'tags' in package['meta'] and 'question' in package['meta']['tags'] and package['meta']['tags']['question']:

            # Get the input message string.
            message_text = str(X[0]).lower()

            # Vectorize the input message using the trained TF-IDF vectorizer.
            vectorized_text = self.tfidf_vectorizer.transform([message_text])

            # Calculate the cosine similarity of a question wrt. to the combined corpus
            cos_similarity = cosine_similarity(self.knowledge_base_vectorized,
                                               vectorized_text).flatten()
            article_index, article_cos_similarity = self.get_matching_article(
                self.common_knowledge_base_clean, cos_similarity)

            # We assign a match as on_topic if it is above or equal to the
            # cosine similarity threshold value.
            if article_cos_similarity >= float(
                    os.environ['KATECHEO_SIMILARITY_THRESHOLD']):

                # Retrieve the body of the matched article.
                X = np.append([self.common_knowledge_base[article_index]['content']], X)
                package['meta']['tags']['on_topic'] = True
                package['meta']['tags']['topic'] = self.common_knowledge_base[article_index]['topic']
                package['meta']['tags']['article_id'] = self.common_knowledge_base[article_index][os.environ['KATECHEO_ARTICLE_ID']]
                package['meta']['tags']['kb_search_error'] = ""
                return X, package
            else:
                package['meta']['tags']['on_topic'] = False
                package['meta']['tags']['topic'] = ""
                package['meta']['tags']['article_id'] = ""
                package['meta']['tags']['kb_search_error'] = 'Could not match "' + message_text + '" to any of the articles from the knowledge base'
                return X, package

        package['meta']['tags']['kb_search_error'] = 'Not enough meta data to proceed'
        return X, package

kbs = KBSearch()

@app.route('/kbsearch', methods=['POST'])
def route_handler():
    response = ""
    X = np.array([request.json['params']])
    package = {
        "meta": request.json["meta"]
    }

    retval = kbs.predict(X, None, package)

    package["params"] = [
        retval[0][0],
        request.json['params']
    ]

    print("KBS package: ", package)

    try:
        r = requests.post("http://localhost:6080/comprehension", data=json.dumps(package), headers={'content-type':'application/json'})
        response = r.text
    except requests.exceptions.RequestException as e:
        print(e)
        pass

    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6070, debug=True)
