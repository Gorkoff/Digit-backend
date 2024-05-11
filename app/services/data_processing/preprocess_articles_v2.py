import pandas as pd
import string
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
from nltk.data import find


def preprocess_articles_v2(data: pd.DataFrame):
    ensure_nltk_resources(["punkt", "stopwords"], ["tokenizers", "corpora"])

    NUM_ARTICLES = len(data)
    NUM_CLUSTERS = round(NUM_ARTICLES / 2)

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


def ensure_nltk_resources(resource_names, directories):
    for resource_name, directory in zip(resource_names, directories):
        try:
            find(f"{directory}/{resource_name}")
        except LookupError:
            nltk.download(resource_name)
