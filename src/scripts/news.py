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


def make_news_request(api_key: str, page_num: int = 0,):
    """This function makes a request to the news api and returns a parsed response"""
    # make a request to the News API
    url = ('https://newsapi.org/v2/everything?')
    parameters = {
        'q': 'the'  # query phrase
        , 'from': today, 'to': today, 'sortBy': 'popularity', 'apiKey': api_key, 'page': page_num
    }
    response = requests.get(url, params=parameters)

    # assert 200 else print error
    assert response.status_code == 200, "Error: {}".format(
        response.status_code)

    parsed_response = json.loads(response.text)
    return parsed_response


def make_corpus_dict(parsed_response):
    """This function takes a the news response and returns a dictionary of sources: articles"""
    json.dumps(parsed_response["articles"])
    corpus_dict = {}
    for i, article in enumerate(parsed_response["articles"]):
        corpus_dict[f'{article["source"]["name"]}_{i}'] = f'{article["title"]}\n{article["description"]}\n{article["content"]}'
    return corpus_dict


def save_corpus(corpus_dict):
    with open(f'../../data/raw_corpus/corpus_{today}.json', 'w') as f:
        json.dump(corpus_dict, f)


def Merge(dict1, dict2):
    """helper function to merge two dictionaries"""
    res = {**dict1, **dict2}
    return res


def news_main():
    corpus_dict = {}
    # one api key only returns 500 articles, we use both api keys to return 1000 for each day
    key_1 = os.getenv("NEWS_API_KEY_1")
    key_2 = os.getenv("NEWS_API_KEY_2")
    for i in range(1, 5):
        try:
            parsed_response = make_news_request(key_1, i)
            corpus_page = make_corpus_dict(parsed_response)
            corpus_dict = Merge(corpus_dict, corpus_page)
            print(f'Page {i} done')
            # wait 10 seconds
            time.sleep(10)
        except:
            print(f'Page {i} failed')

            break
    for i in range(5, 10):
        try:
            parsed_response = make_news_request(key_2, i)
            corpus_page = make_corpus_dict(parsed_response)
            corpus_dict = Merge(corpus_dict, corpus_page)

            print(f'Page {i} done')
            # wait 10 seconds
            time.sleep(10)
        except:
            print(f'Page {i} failed')

            break
    # save corpus
    save_corpus(corpus_dict)
    print('Corpus saved')


if __name__ == "__main__":
    news_main()
