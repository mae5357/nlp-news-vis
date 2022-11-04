# import all other scripts

import news
import preprocessing
import reduce
import vectorization


def main():
    news.news_main()
    preprocessing.preprocessing_main()
    vectorization.vectorization_main("transformer")
    reduce.reducer_main()


if __name__ == "__main__":
    main()
