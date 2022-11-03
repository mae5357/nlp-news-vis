from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import json
import numpy as np
# import umap
import datetime


def load_corpus(path):
    with open(path, 'r') as f:
        corpus = json.load(f)

    return corpus


def dict_to_numpy(corpus_dict):
    # convert dict to numpy array
    data = np.array(list(corpus_dict.values()))
    return data


def reduce(model, data):
    # reduce dimensionality
    model = PCA(n_components=2)
    result = model.fit_transform(data)
    return result


def dimensionalreduction_main(model_type='PCA', embedding_type='transformer'):
    assert model_type in ['PCA', 'TSNE',
                          'UMAP'], 'model_type must be PCA, TSNE or UMAP'
    assert embedding_type in [
        'transformer', 'doc2vec'], 'embedding_type must be transformer or doc2vec'
    # load corpus
    date = datetime.date.today().strftime("%Y-%m-%d")
    corpus = load_corpus(f'../../data/embeddings/{embedding_type}_{date}.json')
    # convert dict to numpy array
    data = dict_to_numpy(corpus)

    if model_type == 'PCA':
        model = PCA(n_components=2)
        results = reduce(model, data)
    elif model_type == 'TSNE':
        model = TSNE(n_components=2, perplexity=50, n_iter=1000,
                     random_state=0, init='pca', learning_rate='auto')
        results = reduce(model, data)
    elif model_type == 'UMAP':
        model = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1,
                          metric='correlation')
        results = reduce(model, data)

    labels = [k.split('_')[0] for k in corpus.keys()]

    # add label as column to results
    results = np.column_stack((results, labels))

    # add header to results
    results = np.insert(results, 0, ['x', 'y', 'label'], axis=0)

    # save results
    np.savetxt(f'../../data/plot_data/{model_type}_{embedding_type}_{date}.csv',
               results, delimiter=',', fmt='%s')


if __name__ == '__main__':
    embedding_type = 'transformer'
    model_type = 'TSNE'
    dimensionalreduction_main(model_type=model_type,
                              embedding_type=embedding_type)
