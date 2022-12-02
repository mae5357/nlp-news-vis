DESCRIPTION - Describe the package in a few paragraphs

The code and datasets included in this package collectively constitute the resources used to implement our news article recommendation system. At a high-level, there is a group of scripts responsible for text vectorization and dimensionality reduction of the datasets, and a set of scripts used to visualize clusters amongst dimensionality reduction model output. A set of news article datasets derived from sources such as HuffPost are also included to be run against the vectorizer/reduction models and visualized accordingly. 

To obtain each of the datasets, NewsAPI's JSON API is interacted with by running the "news.py" script to load titles, descriptions, URLs, and the first couple of sentences from the present day's articles into a JSON file. The "preprocess.py" script is then run to preprocess article text via means including stopword removal and lemma extraction. Running the "vectorize.py" script will then vectorize the preprocessed corpus using a specified transformer model. Lastly, the "reduce.py" script is executed to take the vectorized data and reduce the embeddings to two dimensions via a PCA, t-SNE, or UMAP model. 

After placing the dimensionality-reduced datasets into the directory to be pointed at by the article recommendation system, running the "visualization.js" script will execute our JavaScript-based recommendation application. After starting a Python server and navigating to the local application, users can explore the output of the reduction models via dynamic two-dimensional scatterplots. Specifically, users have the ability to generate scatterplots for one of three pre-generated article datasets using a self-chosen combination of a text vectorizer, dimensionality reduction model, and legend dimension. Additionally, users can click on any two articles (i.e., any two plot points) to generate a similarity score and a comment regarding the likelihood of the user enjoying the articles.

______________________________________________________________________________________________________________
INSTALLATION - How to install and setup your code

Before installation, please complete the following prerequisites:
- Install conda locally
- Install python3 locally
- Create a Kaggle account

After satisfying the prerequisites, you will have to create a virtual environment and install the required dependencies. To do so, enter the following commands into your command prompt/terminal in the specified order:
1) conda create -n venv python=3.8
2) conda activate venv
3) conda install git
4) git config --global user.name "<Your Git username here>"
5) git config --global user.email <Your Git email address here>
6) git clone https://github.com/mae5357/nlp-news-vis
7) cd <The cloned directory>
8) python3 -m pip install -r requirements.txt

After following these instructions, you will be able to execute all code within the cloned repository.
______________________________________________________________________________________________________________
EXECUTION - How to run a demo on your code

To load up the JavaScript application, choose one of the following options:
1) Open a web browser and navigate to: https://rcody8.github.io/
OR
2) Execute 'python3 -m http.server 8888' in a command prompt and then open a web browser to navigate to: http://localhost:8888/docs/ 

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

You will now see the scatterplot repopulate with another 5,000 data points at different coordinate locations, still using Doc2Vec text vectorization. Again, we recommend zooming in by double-clicking on any region of the plot to help emphasize the difference. After doing so, you can again see that you have used the application to redefine the clustering decisions in just two clicks.

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