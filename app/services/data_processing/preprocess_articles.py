# import string
#
# import nltk
# import pandas as pd
# from nltk.corpus import stopwords
# from nltk.stem.snowball import SnowballStemmer
# from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_articles(data):
    return data

    # nltk.download("punkt")
    # nltk.download('stopwords')
    # df = pd.DataFrame(data)
    # df = df.drop(df.columns[[0, 2, 5]], axis=1) #нужно убрать колонки article_id, url, meta_description
    # delimiter = '/. '
    # df['text'] = df.text.str.partition(delimiter)[2]
    # df = df.dropna(subset=["text"])
    # df['currency_curs'] = df['currency_curs'].interpolate()
    # punct = "\n\r" + string.punctuation + '—'
    # df['text'] = df['text'].str.translate(str.maketrans('', '', punct))
    # stop = stopwords.words('russian')
    # df['text'] = df['text'].apply(lambda words: ' '.join(word.lower() for word in words.split() if word not in stop))
    # stemmer = SnowballStemmer('russian')
    # df['text'] = df['text'].apply(lambda words: ' '.join(stemmer.stem(word) for word in words.split()))
    # tfidf_vectorizer = TfidfVectorizer()
    # tfidf_train_vectors = tfidf_vectorizer.fit_transform(df['text'].values)