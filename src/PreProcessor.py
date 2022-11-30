import re
from abc import ABC, abstractmethod
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


class PreProcessor(ABC):

    @abstractmethod
    def preprocess(self, corpus: dict):
        pass


class NltkProcessor(PreProcessor):

    def __init__(self):
        self.en_stop = set(stopwords.words("english"))

    def preprocess(self, corpus):
        for link, doc in corpus.items():
            doc["content"] = self.clean_text(doc.get("content"))

        return corpus


    def clean_text(self, text):
        """
        This function takes a text and returns a list of tokens
        - lowercase
        - remove short words
        - remove stopwords
        - remove extra characters
        - gets root word (lemma)

        """
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if len(token) > 4]  # remove short words
        # remove stopwords
        tokens = [token for token in tokens if token not in self.en_stop]
        # remove extra characters
        tokens = [self.clean_chr(token) for token in tokens]
        tokens = [self.get_lemma2(token) for token in tokens]
        return tokens


    def clean_chr(self, text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        return text


    def get_lemma2(self, word):
        """
        This function takes a word and returns its rootword
        """
        return WordNetLemmatizer().lemmatize(word)