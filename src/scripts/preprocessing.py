
import re
from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import datetime
import json

nltk.download('omw-1.4')


def __init__(self, corpus):
    self.corpus = corpus
    self.stop_words = set(stopwords.words('english'))


def get_lemma2(word):
    from nltk.stem.wordnet import WordNetLemmatizer
    """
    This function takes a word and returns its rootword
    """
    return WordNetLemmatizer().lemmatize(word)

# remove extra characters


def clean_chr(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


def nltk_preprocessing(text):
    """
    This function takes a text and returns a list of tokens
    - lowercase
    - remove short words
    - remove stopwords
    - remove extra characters
    - gets root word (lemma)

    """
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if len(
        token) > 4]      # remove short words
    # remove stopwords
    tokens = [token for token in tokens if token not in en_stop]
    # remove extra characters
    tokens = [clean_chr(token) for token in tokens]
    tokens = [get_lemma2(token) for token in tokens]
    return tokens


def preprocessing_main():
    en_stop = set(stopwords.words('english'))

    # load corpus
    today = datetime.date.today().strftime("%Y-%m-%d")
    with open(f'../../data/raw_corpus/corpus_{today}.json', 'r') as f:
        corpus_dict = json.load(f)

    # create a list of all the articles
    corpus = []
    source = []

    clean_corpus = {}

    for source, doc in corpus_dict.items():
        clean_corpus[source] = nltk_preprocessing(doc)

    # save corpus
    with open(f'../../data/clean_corpus/corpus_{today}.json', 'w') as f:
        json.dump(clean_corpus, f)


if __name__ == "__main__":
    preprocessing_main()
