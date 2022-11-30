# nlp-news-vis

repo for cse6040 group project. 

## Notebook & Vis

See `src/notebooks/news-vis.ipynb` for src notebook.

See https://public.tableau.com/views/newsscatterplotproofofconcept/Sheet1?:showVizHome=no#3 for example visualization.

## Setup

### Make a virtual environment & install dependencies

(assuming you already have conda and python3 installed)
```
git clone git@github.com:mae5357/nlp-news-vis.git
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download data

You might need to make a kaggle account. 

https://www.kaggle.com/datasets/rmisra/news-category-dataset

Place json file `data/` directory.

## Housekeeping

Do not commit data or dependancies to repo (see .gitignore)

Update `requirements.txt` every time you add a package.

Create branches with `{your-name}.{purpose-of-branch}

It would be good to have someone review before merging branches, but this is not strictly necessary.
