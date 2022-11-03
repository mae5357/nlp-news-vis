from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import json
import numpy as np
import umap
import datetime


def load_corpus(path):
    with open(path, "r") as f:
        corpus = json.load(f)

    return corpus


def dict_to_numpy(corpus_dict):
    # convert dict to numpy array
    data = np.array(list(corpus_dict.values()))
    return data


def dimensionalreduction_main(embedding_type="transformer"):
    # load corpus
    date = datetime.date.today().strftime("%Y-%m-%d")
    corpus = load_corpus(f"../../data/embeddings/{embedding_type}_{date}.json")

    # create list of tags
    urls = [k.split("_")[0] for k in corpus.keys()]
    domains = [x.split("/")[2] for x in urls]

    # convert dict to numpy array
    data = dict_to_numpy(corpus)

    model_dict = {
        "PCA": PCA(n_components=2),
        "TSNE": TSNE(
            n_components=2,
            perplexity=50,
            n_iter=500,
            random_state=0,
            init="pca",
            learning_rate="auto",
        ),
        "UMAP": umap.UMAP(
            n_components=2, n_neighbors=10, min_dist=0.1, metric="correlation"
        ),
    }

    for model_type, model in model_dict.items():
        print(f"starting {model_type} on {date}")
        results = model.fit_transform(data)
        # add label as column to results
        results = np.column_stack((results, urls, domains))

        # add header to results
        results = np.insert(results, 0, ["x", "y", "url", "domain"], axis=0)

        # save results
        print(f"saving {model_type} on {date}")
        np.savetxt(
            f"../../data/plot_data/{model_type}_{embedding_type}_{date}.csv",
            results,
            delimiter=",",
            fmt="%s",
        )


if __name__ == "__main__":
    dimensionalreduction_main()
