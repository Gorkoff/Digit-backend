import pandas as pd
from app.services.data_collection import collect_articles
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import warnings
warnings.simplefilter(action='ignore')


from app.services.data_processing.preprocess_articles_v2 import preprocess_articles_v2


def clusterize_articles():
    NUM_CLUSTERS, corpus_embeddings, data = preprocess_articles_v2()
    clustering_model = KMeans(n_clusters=NUM_CLUSTERS)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_

    data['cluster'] = cluster_assignment
    data.head()
    return data


def convert_to_json():
    data = clusterize_articles()
    json_result = data.to_json(orient='records', force_ascii=False)
    return json_result



print(clusterize_articles())
print(convert_to_json())