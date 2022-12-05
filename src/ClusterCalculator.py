import json
import os

from ApiService import NewsIoApi, HuffPostApi
from Vectorizer import Doc2VecVectorizer, BertVectorizer
from DimReducer import PCAReducer, TsneReducer, UmapReducer

RAW_PATH = "../data/raw/"
VEC_PATH = "../data/"


def get_cluster_info():
    FOLDER_PATH = '../data/'

    # get files from folder
    files = [f for f in os.listdir(FOLDER_PATH) if os.path.isfile(
        os.path.join(FOLDER_PATH, f))]

    # only get json files
    files = [f for f in files if f.endswith('.json')]

    article_list = []
    with open('../docs/plots/sample_cluster_scores.csv', 'w') as f:
        f.write(f'file_name, DBS\n')

    for file in files:
        with open(FOLDER_PATH + file, 'r') as f:
            print(f'Processing {file}')
            # load json file using utf-8 encoding
            articles = json.load(f)
            article_list.extend(articles)

            # get coordinates
            coordinates_list = [article['coordinates']
                                for article in article_list]
            category_list = [article['category'] for article in article_list]

            # calculate clusters
            from sklearn.metrics import davies_bouldin_score

            # calculate DBS
            DBS_score = davies_bouldin_score(coordinates_list, category_list)

            print(f'DBS score: {DBS_score}')
            # write to file
            with open('../docs/plots/sample_cluster_scores.csv', 'a') as f:
                f.write(f'{file}, {DBS_score}\n')


def get_samples(vectorizer, reducer, limit):

    # limit
    api = HuffPostApi(limit=limit, rand_sample=True)
    raw_articles = api.get_articles(RAW_PATH + "News_Category_Dataset_v3.json")
    corpus = api.get_corpus_dict(raw_articles)

    # vectorize
    if vectorizer == 'doc2vec':
        vec = Doc2VecVectorizer()
    elif vectorizer == 'bert':
        vec = BertVectorizer()

    vectors = vec.vectorize(corpus)

    # reduce

    if reducer == 'None':
        return vectors
    elif reducer == 'pca':
        reducer = PCAReducer()
    elif reducer == 'tsne':
        reducer = TsneReducer()
    elif reducer == 'umap':
        reducer = UmapReducer()

    # reduce using UmapReducer
    dr = UmapReducer()
    corpus_coordinates = dr.dimreduce(vectors)
    for link, coord in corpus_coordinates.items():
        corpus[link]["coordinates"] = coord

    # save to file
    api.save(VEC_PATH + f"{limit}.json", list(corpus.values()))


if __name__ == "__main__":
    # import matrix.csv
    # import pandas as pd
    import pandas as pd

    vectorizer = 'doc2vec'
    reducer = 'none'
    limit = 100

    vector = get_samples(vectorizer, reducer, limit)

    # save to file
    df = pd.DataFrame(vector)
    df.to_csv(f'../data/{vectorizer}_{reducer}_{limit}.csv', index=False)

    df = pd.read_csv('../data/matrix.csv')

    for row in df.iterrows():
        vectorizer = row['vectorizer']
        reducer = row['reducer']
        limit = row['limit']

        limit_samples(vectorizer, reducer, limit)
