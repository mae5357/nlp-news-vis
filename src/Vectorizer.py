from abc import ABC, abstractmethod

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument


class Vectorizer(ABC):

    @abstractmethod
    def vectorize(self, corpus: dict):
        pass


class Doc2VecVectorizer(Vectorizer):

    def __init__(self, nspace=700, window=5, min_count=1, workers=4, epochs=100):
        self.nspace = nspace
        self.window = window
        self.min_count = min_count
        self.workers = workers
        self.epochs = epochs

    def vectorize(self, corpus):
        tagged_corpus = self.get_tagged_corpus(corpus)

        model = Doc2Vec(
            documents=tagged_corpus,
            vector_size=self.nspace,
            window=self.window,
            min_count=self.min_count,
            workers=self.workers,
            epochs=self.epochs
        )

        return {doc.tags: model.infer_vector(doc.words).tolist() for doc in tagged_corpus}


    def get_tagged_corpus(self, corpus):
        tagged_corpus = []

        for link, doc in corpus.items():
            tagged_corpus.append(TaggedDocument(words=doc["content"], tags=link))

        return tagged_corpus
