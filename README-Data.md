# How Processed Data Files Are Created

## Processing Structure
The processing portion of the project is broken into 4 major areas:
- ApiService:  These are the classes for getting articles from either an external api service or from the downloaded Kaggle dataset.
- PreProcessor:  Nltk class for cleaning and tokenizing (removing stop-words, special characters, etc). Only Doc2Vec uses the PreProcessor, Bert uses the full, raw article text.
- Vectorizer:  Doc2Vec and Bert classes that transform the text into vectors.
- DimReducer:  These are the classes that reduce the high-count vectors down to just (x, y) coordinates.

## Example Notebook/Script Steps
The following is also already included in a `sandbox.py` file.

    # Create an ApiService to get/save articles.
    # The services that hit external api's require an api_key.
    # Additionally, other constructor args may be passed such as a limit for HuffPost.
    api = HuffPostApi()

    # Get articles from api url (or from previously created file, as is the case with this example).
    # By default the HuffPostApi reads whole file but only returns top 1000 articles
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

# File Naming/Formatting for Front-End
The front-end expects files to be stored in `/docs/data` and to be named in the form of `dataset.preprocessor.vectorizer.reducer.json` in order to display the various permutations.
Below is an example json object the front-end expects (i.e., an example from the above `list(cleaned_corpus.values())`)

```
{
    "title": "Sri Lanka President, Prime Minister To Resign Amid Civil Unrest",
    "link": "https://www.huffpost.com/entry/prime-minister-ranil-wickremesinghe-sri-lanka-quit_n_62c98ef3e4b02e0ac914b425",
    "description": "President Gotabaya Rajapaksa has agreed to resign as of Wednesday.",
    "content": "Sri Lanka President, Prime Minister To Resign Amid Civil Unrest President Gotabaya Rajapaksa has agreed to resign as of Wednesday.",
    "date": "2022-07-09",
    "source": "HuffPost",
    "category": "WORLD NEWS",
    "authors": "Krishan Francis, AP",
    "vectors": null,
    "coordinates":
    [
        2.9825501441955566,
        13.54939079284668
    ]
}
```