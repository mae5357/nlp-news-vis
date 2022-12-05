from ApiService import NewsIoApi, HuffPostApi
from PreProcessor import NltkProcessor
from Vectorizer import Doc2VecVectorizer, BertVectorizer
from DimReducer import PCAReducer, TsneReducer, UmapReducer

RAW_PATH = "../data/raw/"
CLEAN_PATH = "../data/cleaned/"
VEC_PATH = "../data/vectorized/"
RED_PATH = "../data/reduced/"

if __name__ == "__main__":
    # Create an ApiService to get/save articles.
    # The services that hit external api's require an api_key.
    # Additionally, other constructor args may be passed such as a limit for HuffPost.
    api = HuffPostApi()

    # Get articles from api url (or from previously created file, as is the case with this example).
    # By default, the HuffPostApi reads whole file but only returns top 1000 articles
    # (this limit can be changed in the constructor/object instantiation).
    raw_articles = api.get_articles(RAW_PATH + "huffpost.json")

    # The articles need to be formatted to a standard output that the front-end expects.
    # Each ApiService contains logic to do this formatting (essentially maps fields),
    # and converts to dict using article url as keys ({article_url: {title: ..., date: ..., etc}}).
    corpus = api.get_corpus_dict(raw_articles)

    # Create a PreProcessor to clean text from the previous corpus dict
    # and save if desired.
    # Note, only Doc2Vec uses this step, BERT pulls straight from raw article text.
    pproc = NltkProcessor()
    cleaned_corpus = pproc.preprocess(corpus)
    api.save(CLEAN_PATH + "huffpost1000.nltk.json", cleaned_corpus)

    # Create Vectorizor, vectorize cleaned_corpus (or just corpus for BERT)
    # and save if desired.
    # This returns a dict of {link: vectors[]} to be reduced an mapped
    # back into the corpus dict later.
    # This means both a corpus dict and these vectors will be merged back together in
    # the final step.
    vec = Doc2VecVectorizer()
    vectors = vec.vectorize(cleaned_corpus)
    api.save(VEC_PATH + "huffpost1000.nltk.doc2vec.json", vectors)

    # Create a DimReducer, reduce vectors, and save results back into corpus objects.
    # Note, since this eventually needs to be list of objects, doing that here.
    dr = PCAReducer()
    corpus_coordinates = dr.dimreduce(vectors)
    for link, coord in corpus_coordinates.items():
        cleaned_corpus[link]["coordinates"] = coord
    api.save(RED_PATH + "huffpost1000.nltk.doc2vec.pca.json", list(cleaned_corpus.values()))