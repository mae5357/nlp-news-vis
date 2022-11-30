# Team 120 Paranormal Distribution
## See the main repo for additional instructions, this is mainly a guide for spinning up the visualization.

# Quick Start
- Get a simple python server going: `python3 -m http.server 8888`
- Navigate to the app: `http://localhost:8888/docs/`

You should now be on the landing page looking at some data!
The data is just served up from pre-processed files, nothing is processed in real-time.

If you'd like to experiment with addional datasets or tweaking NLP params, feel free to leverage the classes in the `src` folder (I use the `sandbox.py` file as a kind of "notebook" to process the articles as needed) or generate on your own.  Just make sure to save them in the file and format specified below:
- Save final files in `/docs/data/` (note that /docs is /app in the main repo, github pages needs /docs)
- Save files in the naming format `datasetName.preprocessorName.vectorizerName.reducerName.json`.  (Note that new datasets will need to be manually included in the list in `index.html`)
