# Team 120 Paranormal Distribution

## Quick Start
- Get a simple python server going: `python3 -m http.server 8888`
- Navigate to the app: `http://localhost:8888/docs/`

You should now be on the landing page looking at some data!
The data is just served up from pre-processed files, nothing is processed in real-time.

If you'd like to experiment with addional datasets or tweaking NLP params, feel free to leverage the classes in the `src` folder (I use the `sandbox.py` file as a kind of "notebook" to process the articles as needed) or generate on your own.  Just make sure to save them in the file and format specified below:
- Save final files in `/docs/data/` (note that /docs is /app in the main repo, github pages needs /docs)
- Save files in the naming format `datasetName.preprocessorName.vectorizerName.reducerName.json`.  (Note that new datasets will need to be manually included in the list in `index.html`)

## Notebook & Vis

See `src/notebooks/news-vis.ipynb` for src notebook.

See https://public.tableau.com/views/newsscatterplotproofofconcept/Sheet1?:showVizHome=no#3 for example visualization.

## Setup

### Make a virtual environment & install dependencies

(assuming you already have conda and python3 installed)
```bash
git clone https://github.com/mae5357/nlp-news-vis
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download data

You might need to make a kaggle account. 

https://www.kaggle.com/datasets/rmisra/news-category-dataset

Place json file `data/` directory.
