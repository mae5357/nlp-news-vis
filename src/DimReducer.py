from abc import ABC, abstractmethod

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP


class DimReducer(ABC):

    @abstractmethod
    def dimreduce(self, corpus: dict):
        pass


class PCAReducer(DimReducer):

    def __init__(self, n_components=2):
        self.n_components = n_components


    def dimreduce(self, corpus: dict):
        # convert dict to numpy array
        data = np.array(list(corpus.values()))

        model = PCA(n_components=self.n_components)
        results = model.fit_transform(data)

        return dict(zip(corpus.keys(), results.tolist()))


class TsneReducer(DimReducer):

    def __init__(self, n_components=2, perplexity=50, n_iter=500, random_state=0, init="pca", learning_rate="auto"):
        self.n_components = n_components
        self.perplexity = perplexity
        self.n_iter = n_iter
        self.random_state = random_state
        self.init = init
        self.learning_rate = learning_rate

    def dimreduce(self, corpus: dict):
        # convert dict to numpy array
        data = np.array(list(corpus.values()))

        model = TSNE(
            n_components=self.n_components,
            perplexity=self.perplexity,
            n_iter=self.n_iter,
            random_state=self.random_state,
            init=self.init,
            learning_rate=self.learning_rate
        )
        results = model.fit_transform(data)

        return dict(zip(corpus.keys(), results.tolist()))


class UmapReducer(DimReducer):

    def __init__(self, n_components=2, n_neighbors=10, min_dist=0.1, metric="correlation"):
        self.n_components = n_components
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.metric = metric

    def dimreduce(self, corpus: dict):
        # convert dict to numpy array
        data = np.array(list(corpus.values()))

        model = UMAP(
            n_components=self.n_components,
            n_neighbors=self.n_neighbors,
            min_dist=self.min_dist,
            metric=self.metric
        )
        results = model.fit_transform(data)

        return dict(zip(corpus.keys(), results.tolist()))