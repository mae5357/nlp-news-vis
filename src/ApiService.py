import json
import os
import time
from abc import ABC, abstractmethod
from datetime import date

import requests
from dotenv import load_dotenv


class ApiService(ABC):

    @abstractmethod
    def get_articles(self, page_start, page_end):
        pass

    @abstractmethod
    def get_corpus_dict(self, articles):
        pass

    def get_from_file(self, path):
        with open(path, 'r') as f:
            data = f.read()
        return json.loads(data)

    def save(self, path: str, articles):
        with open(path, "w") as f:
            json.dump(articles, f)


class NewsApi(ApiService):

    def __init__(self):
        load_dotenv()
        self.today = date.today().strftime("%Y-%m-%d")

    def get_articles(self, page_start=1, page_end=10):
        # one api key only returns 500 articles, we use both api keys to return 1000 for each day
        split_page = int(page_end / 2)
        api_dict = self.merge(
            {p: os.getenv("NEWS_API_KEY_1") for p in range(page_start, split_page)},
            {p: os.getenv("NEWS_API_KEY_2") for p in range(split_page, page_end)},
        )

        # iterate through each page of the api
        articles = []
        for page_num, api_key in api_dict.items():
            try:
                articles.extend(self.make_news_request(api_key, page_num))
                # corpus_dict = self.merge(corpus_dict, self.make_corpus_dict(articles))
                print(f"page {page_num} of 10")
                time.sleep(1)
            except:
                print(f"Error on page {page_num}")
                continue

        return articles


    def get_corpus_dict(self, raw_articles):
        return self.make_corpus_dict(raw_articles)


    def make_news_request(self, api_key: str, page_num: int = 0):
        """This function makes a request to the news api and returns a parsed response"""
        # source https://newsapi.org/
        # make a request to the News API
        url = "https://newsapi.org/v2/everything?"
        parameters = {
            "q": "the",  # query phrase
            "from": self.today,
            "to": self.today,
            "sortBy": "popularity",
            "apiKey": api_key,
            "page": page_num,
        }
        response = requests.get(url, params=parameters)

        # assert 200 else print error
        assert response.status_code == 200, "Error: {}".format(response.status_code)

        parsed_response = json.loads(response.json().get('articles'))
        return parsed_response


    def make_corpus_dict(self, articles):
        corpus_dict = {}
        for article in articles:
            try:
                corpus_dict[article["url"]] = {
                    "title": article.get("title") or None,
                    "link": article.get("url"),
                    "description": article.get("description") or None,
                    "content": article.get("desciption") or None,
                    "date": article.get("publishedAt").split("T")[0] if article.get("publishedAt") else None,
                    "source": article.get("source").get("name") or None,
                    "category": None,
                    "authors": article.get("author") or None,
                    "vectors": None,
                    "coordinates": None
                }
            except Exception as e:
                print(e)
                continue

        return corpus_dict


    def merge(self, dict1, dict2):
        """helper function to merge two dictionaries"""
        res = {**dict1, **dict2}
        return res


class NewsIoApi(ApiService):

    def __init__(self, api_key):
        self.today = date.today().strftime("%Y-%m-%d")
        self.api_key = api_key
        self.url = f'https://newsdata.io/api/1/news?apikey={self.api_key}&country=us&language=en&domain=cnn,npr,foxnews,nypost,espn'


    def get_articles(self, page_start=1, page_end=51):
        articles = []
        for page in range(page_start, page_end):
            res = requests.get(f'{self.url}&page={page}')
            articles.extend(res.json().get('results'))

        return articles


    def get_corpus_dict(self, raw_articles):
        corpus_dict = {}
        for article in raw_articles:
            try:
                corpus_dict[article["link"]] = {
                    "title": article.get("title") or None,
                    "link": article.get("link") or None,
                    "description": article.get("description") or None,
                    "content": article.get("content") or None,
                    "date": article.get("pubDate").split(" ")[0] if article.get("pubDate") else None,
                    "source": article.get("source_id") or None,
                    "category": article.get("category")[0] if article.get("category") else None,
                    "authors": ", ".join(article["authors"]) if article.get("authors") else None,
                    "vectors": None,
                    "coordinates": None
                }
            except Exception as e:
                print(e)
                continue

        return corpus_dict


    def get_articles_with_content(self, articles):
        articles_content = []
        for article in articles:
            try:
                # if article.get('content') and len(article.get('content')) > len(article.get('description')):
                if article.get('content') and len(article.get('content')) > 1500:
                    articles_content.append(article)
            except Exception as e:
                print(e)
                continue

        return articles_content


class HuffPostApi(ApiService):

    def __init__(self, limit=1000):
        self.limit = limit

    def get_articles(self, path):
        articles_json = self.get_from_file(path)

        if self.limit:
            articles_json = articles_json[:self.limit]

        return articles_json


    def get_corpus_dict(self, raw_articles):
        corpus_dict = {}
        for article in raw_articles:
            try:
                if len(article.get("headline")) + len(article.get("short_description")) < 50:
                    continue
                corpus_dict[article["link"]] = {
                    "title": article.get("headline") or None,
                    "link": article.get("link") or None,
                    "description": article.get("short_description") or None,
                    "content": f'{article.get("headline")} {article.get("short_description")}',
                    "date": article.get("date") or None,
                    "source": None,
                    "category": article.get("category") or None,
                    "authors": article.get("authors") or None,
                    "vectors": None,
                    "coordinates": None
                }
            except Exception as e:
                print(e)
                continue

        return corpus_dict
