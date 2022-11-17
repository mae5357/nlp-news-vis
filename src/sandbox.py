from ApiService import NewsIoApi, HuffPostApi
from PreProcessor import NltkProcessor
from Vectorizer import Doc2VecVectorizer
from DimReducer import PCAReducer, TsneReducer

RAW_PATH = "../data/raw/"
CLEAN_PATH = "../data/cleaned/"
VEC_PATH = "../data/vectorized/"
RED_PATH = "../data/reduced/"

if __name__ == "__main__":
    # create an ApiService to get/save articles
    api = HuffPostApi()

    # get articles from api (or more commonly from previously pulled file)
    # by default the HuffPostApi reads whole file but only returns top 1000 articles
    # (this limit can be changed in the constructor for now)
    raw_articles = api.get_articles(RAW_PATH + "huffpost.json")

    # the articles need to be formatted to a standard output that naively maps fields,
    # and converts to dict using url/link as keys
    corpus = api.get_corpus_dict(raw_articles)

    # create a PreProcessor to clean text and save if desired
    pproc = NltkProcessor()
    cleaned_corpus = pproc.preprocess(corpus)
    api.save(CLEAN_PATH + "huffpost1000.nltk.json", cleaned_corpus)

    # create Vectorizor and save if desired
    # at the moment this returns dict of link: vectors[] to be reduced an mapped
    # back into the corpus json later. contemplating shoving them back into objects.
    vec = Doc2VecVectorizer()
    vectors = vec.vectorize(cleaned_corpus)
    api.save(VEC_PATH + "huffpost1000.nltk.doc2vec.json", vectors)

    # create a DimReducer and save results back into corpus objects
    # since this eventually needs to be list of objects, doing that here
    dr = PCAReducer()
    corpus_coordinates = dr.dimreduce(vectors)
    for link, coord in corpus_coordinates.items():
        cleaned_corpus[link]["coordinates"] = coord
    api.save(RED_PATH + "huffpost1000.nltk.doc2vec.pca.json", cleaned_corpus.values())

