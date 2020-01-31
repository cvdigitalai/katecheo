import os
import re
import copy
import json
import nltk

nltk.download('stopwords')
nltk.download('punkt')

import string
import urllib
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


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
            urllib.request.urlretrieve(kb_url, os.path.basename(kb_url))

            # Load the downloaded JSON files.
            with open(os.path.basename(kb_url)) as f:
                knowledge_bases_raw_data[topic] = json.load(f)

        # Iterate through each article from each topic and get only the
        # article ID, title and body of each article.
        for topic in knowledge_bases_raw_data:
            for article in knowledge_bases_raw_data[topic]:
                if os.environ['ARTICLE_ID'] and os.environ[
                        'ARTICLE_TITLE_KEY'] and os.environ['ARTICLE_BODY_KEY']:
                    self.common_knowledge_base.append({
                        os.environ['ARTICLE_ID']:
                        article[os.environ['ARTICLE_ID']],
                        "content":
                        article[os.environ['ARTICLE_TITLE_KEY']] + " " +
                        article[os.environ['ARTICLE_BODY_KEY']],
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

    def predict(self, X, feature_names, meta):
        if 'tags' in meta and 'question' in meta['tags'] and meta['tags'][
                'question']:

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
                    os.environ['COSINE_SIMILARITY_THRESHOLD']):

                # Retrieve the body of the matched article.
                X = np.append(
                    [self.common_knowledge_base[article_index]['content']], X)
                self.result['on_topic'] = True
                self.result['topic'] = self.common_knowledge_base[
                    article_index]['topic']
                self.result['article_id'] = self.common_knowledge_base[
                    article_index][os.environ['ARTICLE_ID']]
                self.result['kb_search_error'] = ""
                return X
            else:
                self.result['on_topic'] = False
                self.result['topic'] = ""
                self.result['article_id'] = ""
                self.result[
                    'kb_search_error'] = 'Could not match "' + message_text + '" to any of the articles from the knowledge base'
                return X
        else:
            self.result = meta['tags']
            return X

    def tags(self):
        return self.result
