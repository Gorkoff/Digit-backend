import pandas as pd
import string
import json

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

import nltk
from nltk.corpus import stopwords


def preprocess_articles_v2():
    nltk.download("punkt")
    nltk.download('stopwords')

    NUM_ARTICLES = 400
    NUM_CLUSTERS = int(NUM_ARTICLES / 2)

    data = pd.read_csv('tass_edited.csv')

    data = data.drop(data.columns[[0, 1, 3, 5, 6]], axis=1)

    delimiter = '/. '
    data.text = data.text.str.partition(delimiter)[2]
    data.text.head()

    data = data.dropna(subset=["text"])
    data.text.isna().sum()
    data = data.interpolate()
    print('Количество пустых значений:', data.currency_curs.isna().sum())
    data.isna().values.any()

    data = data[:NUM_ARTICLES]

    punct = "\n\r" + string.punctuation + '—'
    data['text'] = data['text'].str.translate(str.maketrans('', '', punct))
    stop = stopwords.words('russian')
    data['text'] = data['text'].apply(
        lambda words: ' '.join(word.lower() for word in words.split() if word not in stop))

    indexes = data[data.text == ''].index
    data = data.drop(indexes)
    data.head()

    embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    corpus = list(data['text'])
    corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)

    return NUM_CLUSTERS, corpus_embeddings, data
