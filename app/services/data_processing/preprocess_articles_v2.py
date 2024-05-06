import pandas as pd
import string
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords


def preprocess_articles_v2(data: pd.DataFrame):
    nltk.download("punkt")
    nltk.download('stopwords')

    NUM_ARTICLES = len(data)
    NUM_CLUSTERS = int(NUM_ARTICLES / 2)

    delimiter = '/. '
    data.text = data.text.str.partition(delimiter)[2]

    punct = "\n\r" + string.punctuation + '—'
    data['text'] = data['text'].str.translate(str.maketrans('', '', punct))
    stop = stopwords.words('russian')
    data['text'] = data['text'].apply(
        lambda words: ' '.join(word.lower() for word in words.split() if word not in stop))

    indexes = data[data.text == ''].index
    data = data.drop(indexes)

    embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    corpus = data['text'].tolist()
    corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)

    return NUM_CLUSTERS, corpus_embeddings, data


