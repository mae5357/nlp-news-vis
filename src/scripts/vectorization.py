from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import sys
import numpy as np
import json

from sentence_transformers import SentenceTransformer
# nltk.download('omw-1.4')


en_stop = set(stopwords.words('english'))

# parent class for saving np array in json


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Corpus(object):
    def __init__(self, path) -> None:
        self.path = path
        self.stop_words = set(stopwords.words('english'))
        self.corpus = self.load_corpus()
        self.tagged_corpus = self.tagged_corpus()

    def load_corpus(self):
        with open(self.path, 'r') as f:
            corpus = json.load(f)

        return corpus

    def tagged_corpus(self):
        # add tags to each document
        return [TaggedDocument(words=text, tags=tags)
                for tags, text in self.corpus.items()]

    def doc2Vec(self):
        n_space = 700
        tagged_corpus = self.tagged_corpus
        model_d2v = Doc2Vec(
            documents=tagged_corpus,
            vector_size=n_space,
            window=5,
            min_count=1,
            workers=4,
            epochs=100)

        return {doc.tags: model_d2v.infer_vector(doc.words) for doc in tagged_corpus}

    def sentence_tranformer(self, model='sentence-transformers/all-mpnet-base-v2'):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(model)
        corpus = self.corpus
        # make corpus list of strings
        corpus = [' '.join(text) for text in corpus.values()]
        vectors = model.encode(corpus)

        # get tags from corpus
        tags = [doc.tags for doc in self.tagged_corpus]

        # make corpus dict
        corpus_dict = {tag: vector for tag, vector in zip(tags, vectors)}
        return corpus_dict


def vectorization_main(model):
    import datetime
    date = datetime.date.today().strftime("%Y-%m-%d")
    corpus = Corpus(path=f'../../data/clean_corpus/corpus_{date}.json')

    # if sys arg is 'doc2vec' then run doc2vec
    if model == 'doc2vec':
        corpus_dict = corpus.doc2Vec()
        print(len(corpus_dict))
        with open(f'../../data/embeddings/doc2vec_{date}.json', 'w') as f:
            json.dump(corpus_dict, f, cls=NumpyArrayEncoder)
    elif model == 'transformer':
        corpus_dict = corpus.sentence_tranformer()
        print(len(corpus_dict))
        with open(f'../../data/embeddings/transformer_{date}.json', 'w') as f:
            json.dump(corpus_dict, f, cls=NumpyArrayEncoder)


if __name__ == "__main__":
    vectorization_main(model='transformer')
