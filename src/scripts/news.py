from datetime import date
import requests
import os
import json
import time


# load environment variables
from dotenv import load_dotenv

load_dotenv()

# get today's date
today = date.today().strftime("%Y-%m-%d")


def make_news_request(api_key: str, page_num: int = 0):
    """This function makes a request to the news api and returns a parsed response"""
    # source https://newsapi.org/
    # make a request to the News API
    url = "https://newsapi.org/v2/everything?"
    parameters = {
        "q": "the",  # query phrase
        "from": today,
        "to": today,
        "sortBy": "popularity",
        "apiKey": api_key,
        "page": page_num,
    }
    response = requests.get(url, params=parameters)

    # assert 200 else print error
    assert response.status_code == 200, "Error: {}".format(response.status_code)

    parsed_response = json.loads(response.text)
    return parsed_response


def make_corpus_dict(parsed_response):
    json.dumps(parsed_response["articles"])
    corpus_dict = {}
    for article in parsed_response["articles"]:
        corpus_dict[
            f'{article["url"]}'
        ] = f'{article["title"]}\n{article["description"]}\n{article["content"]}'
    return corpus_dict


def save_corpus(corpus_dict):
    with open(f"../../data/raw_corpus/corpus_{today}.json", "w") as f:
        json.dump(corpus_dict, f)


def Merge(dict1, dict2):
    """helper function to merge two dictionaries"""
    res = {**dict1, **dict2}
    return res


def news_main():
    corpus_dict = {}
    # one api key only returns 500 articles, we use both api keys to return 1000 for each day
    api_dict = Merge(
        {p: os.getenv("NEWS_API_KEY_1") for p in range(1, 5)},
        {p: os.getenv("NEWS_API_KEY_2") for p in range(5, 10)},
    )

    # iterate through each page of the api
    for page_num, api_key in api_dict.items():
        try:
            parsed_response = make_news_request(api_key, page_num)
            corpus_dict = Merge(corpus_dict, make_corpus_dict(parsed_response))
            print(f"page {page_num} of 10")
            time.sleep(1)
        except:
            print(f"Error on page {page_num}")
            continue

    # save corpus
    save_corpus(corpus_dict)
    print("Corpus saved: " + len(corpus_dict))


if __name__ == "__main__":
    news_main()
