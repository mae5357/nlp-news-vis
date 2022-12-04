## DESCRIPTION

The code and datasets included in this package collectively constitute the resources used to implement our news article recommendation system. At a high-level, there is a group of scripts responsible for text vectorization and dimensionality reduction of the datasets, and a set of javascript/css used to visualize model output. A set of news article datasets derived from Kaggle and the NewsData.io API are also included to be run against the vectorizer/reduction models and visualized accordingly.

The text-processing python code in "/src" consists of interfaces/classes that can be used to create a pipeline of dataset -> pre-processor -> vectorizer -> reducer -> output for visual. The process involves instantiating a class for each step of the pipeline to retrieve articles, process, format, and save to serve up to the front-end. These steps are not required to run/use the application since we asynchronously created all the necessary files and publicly hosted the application, but more details can be found in the README-Data.md file to build everything from scratch.

The front-end visualization takes the processed/formatted files from the python output and serves them via the html/javascript/css in the "/docs" folder. By accessing the public site (https://rcody8.github.io/) or starting a Python server and navigating to the local application (/docs), users can explore the output of the reduction models via dynamic two-dimensional scatterplots. Specifically, users have the ability to generate scatterplots for one of three pre-generated article datasets using a self-chosen combination of a text vectorizer, dimensionality reduction model, and legend dimension. Additionally, users can click on any two articles (i.e., any two plot points) to generate a similarity score for more quantitative feedback.

______________________________________________________________________________________________________________
## INSTALLATION
### NOTE:  Insallation is only required to run/access the app locally.  It can be accessed and explored via the public site https://rcody8.github.io/

Before installation, please complete the following prerequisites:
- Install conda locally
- Install python3 locally
- Create a Kaggle account

After satisfying the prerequisites, you will have to create a virtual environment and install the required dependencies. To do so, enter the following commands into your command prompt/terminal in the specified order:
1) `conda create -n venv python=3.8`
2) `conda activate venv`
3) `python3 -m pip install -r requirements.txt` (from inside the CODE directory where the requirements.txt file is located)

Optionally:
3) `conda install git`
4) `git config --global user.name "<Your Git username here>"`
5) `git config --global user.email <Your Git email address here>`
6) `git clone https://github.com/mae5357/nlp-news-vis`
7) `cd <The cloned directory>`
8) `python3 -m pip install -r requirements.txt`

After following these instructions, you will be able to execute all code within the repository.
______________________________________________________________________________________________________________
## EXECUTION

To load up the JavaScript application, choose one of the following options:
1) Open a web browser and navigate to: https://rcody8.github.io/
   OR
2) Execute `python3 -m http.server 8888` in a command prompt and then open a web browser to navigate to: http://localhost:8888/docs/

After following one of those steps, you will be looking at the news article recommendation system. The landing page will display a two-dimensional scatterplot based on a dataset containing 1,000 randomly sampled news articles from HuffPost ("HuffPost1000"). HuffPost1000's text data has already been preprocessed, vectorized using a SentenceBERT model, and dimensionality-reduced using a UMAP model. The default scatterplot displays all reduced data points using a legend with a color-coded key based on article topics.

Let's generate another scatterplot using a different dataset. To do so, follow these steps:
1) In the navigation bar, locate and click the button that says "Dataset"
2) Click on the "HuffPost5000" option

You should see the scatterplot repopulate at this point with 5,000 data points, cumulatively representative of 5,000 randomly sampled HuffPost news articles.

Now let's change the text vectorizer used to vectorize the raw article corpora:
1) In the navigation bar, locate and click the button that says "Vectorizer"
2) Click on the "Doc2Vec" option

You should see the scatterplot repopulate with another 5,000 data points, but at different coordinates than the previous plot. If this is tough to see at a glance, try zooming into the plot by double-clicking anywhere within it or using your mouse's scroll wheel. After doing so, you can easily see that you have used the application to redefine the clustering decisions displayed in the visualization in just a couple of clicks.

To change the dimensionality reduction model used to process the article corpus, the overall process is identical:
1) In the navigation bar, locate and click the button that says "Reducer"
2) Click on the "PCA" option

You will now see the scatterplot repopulate with the same 5,000 data points at different coordinate locations, still using Doc2Vec text vectorization. Again, we recommend zooming in by double-clicking on any region of the plot to help emphasize the difference. After doing so, you can again see that you have used the application to redefine the clustering decisions in just two clicks.

At this point, the legend is still configured to color-code news articles by topic. However, you can customize the legend to color-code data points along several different dimensions. As an example, follow these steps:
1) In the navigation bar, locate and click the button that says "Legend"
2) Click on the "Date" button

The number and location of data points in the scatterplot should remain unchanged, but the plot's legend should now display a list of keys based on article publication months. Consequently, the colors of all visualized articles will have changed to reflect the modified legend dimension.

The application also provides granular control over the legend. For instance, using the date-based legend, what if we wanted to only visualize the cluster containing articles published during August 2022? To do this:
1) At the top of the legend, click "Show/Hide All"
2) Click the circle next to the key that says "2022-8"

The scatterplot should now only contain several news articles, as the other plot points have been hidden. To confirm that all of the remaining articles were published during August 2022, click on any of the data points and look at the "Date" section of the tooltip that pops up! The tooltip will also contain other article metadata for attributes such as an article's title and source.

Lastly, the application can generate similarity scores between any two news articles. For example, try the following:
1) Hold down the SHIFT key on your keyboard
2) While holding down the SHIFT key, click on any data point
3) While holding down the SHIFT key, click on another data point

After doing this, two distance scores will be generated: Euclidean distance and Cosine similarity. Given two news articles, a smaller Euclidean distance would suggest that if you enjoy reading one article, you would likely enjoy reading the other, while the inverse is also true. Alternatively, a larger Cosine similarity would also suggest that if you enjoy reading one article, you would likely enjoy reading the other, with the inverse also being true.