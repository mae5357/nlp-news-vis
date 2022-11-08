from abc import ABC, abstractmethod

import numpy as np
from sklearn.decomposition import PCA


class DimReducer(ABC):

    @abstractmethod
    def dimreduce(self, corpus: dict):
        pass


class PCAReducer(DimReducer):

    def __init__(self, ncomponents=2):
        self.ncomponents = ncomponents


    def dimreduce(self, corpus: dict):
        # convert dict to numpy array
        data = np.array(list(corpus.values()))

        model = PCA(self.ncomponents)
        results = model.fit_transform(data)

        return dict(zip(corpus.keys(), results.tolist()))
