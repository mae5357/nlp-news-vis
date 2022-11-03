# import all other scripts

from . import news, preprocessing, reduce, vectorization


def main():
    news.news_main()
    preprocessing.preprocessing_main()
    vectorization.vectorization_main()
    reduce.reduce_main()


if __name__ == "__main__":
    main()
