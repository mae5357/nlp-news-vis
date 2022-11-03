# News

We are using [this news API](https://newsapi.org/) to get news articles.

Unfotunately this API is limited in the number of articles it can give us, but making API keys is free with multiple emails. 

Store at least 2 API keys stored in a `.env` in the root folder:

```bash
NEWS_API_KEY_1=b068e...
NEWS_API_KEY_2=d2659...
```
The script will pull the article title, description, and first couple sentences along with the article url. We save the data as a json file in `data/raw_corpus` directory with structure:

```python
{
    {"article-url"}: {"title\n description\nfirst couple sentences"}
}
```

for example:
```json
{"https://lifehacker.com/these-are-the-best-store-bought-pie-crusts-1849737398": "These Are the Best Store-Bought Pie Crusts\nDessert is always last\u2014in eating order, but also on the priority prep list. Preparing the Thanksgiving turkey and a diverse list of sides is enough to pull the cook\u2019s focus away from the pies on the menu. Enter: the store-bought pie crust, the fast and easy w\u2026\nDessert is always lastin eating order, but also on the priority prep list. Preparing the Thanksgiving turkey and a diverse list of sides is enough to pull the cooks focus away from the pies on the me\u2026 [+5122 chars]", ...}
```

Run this script to get save today's news in `data/raw_corpus` directory:

```python
python3 news.py
```

# Preprocessing

This script goes through some preprocessing steps:
    - lowercase
    - remove short words
    - remove stopwords
    - remove extra characters
    - gets root word (lemma)

Run this script to get save today's news in `data/clean_corpus` directory:

```python
python3 preprocess.py
```
** note that if you are doing transormer-based vectorization you should not preprocess the data. Instead perform the transformations on the raw data.
# Vectorization

Now we are ready to vectorize our corpus. 

** note that if you are doing transormer-based vectorization you should not preprocess the data. Instead perform the transformations on the raw data.

## Doc2Vec

Here we use [gensim](https://radimrehurek.com/gensim/) to vectorize our corpus.

## Transformer

We can use any transformer model from [HuggingFace](https://huggingface.co/transformers/pretrained_models.html) to vectorize our corpus. Our defualt is `sentence-transformers/all-mpnet-base-v2` but you can change this in  `vectorization.sentence_tranformer` function.

Run this script to get save today's news in `data/embeddings` directory:

```python
python3 vectorize.py
```
Default model is transformers. 

# Dimensionality Reduction

Finally we can reduce the embeddings to 2 dimensions. We can use PCA, t-SNE, or UMAP.

Run this script to get save today's news in `data/plot_data` directory:

```python
python3 reduce.py
```
Default model is t-sne.

todo: (still need to make umap package work)

# Final Data

The final data is stored in `data/plot_data` directory. It is a csv file with the following columns:

```python
x-corrdinate, y-coordinate, article-url, domain (new source)
```

