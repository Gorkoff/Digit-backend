import pandas as pd
from app.services.data_collection import collect_articles
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def clusterize_articles(preprocessed_articles):
    # Кластеризация статей на основе TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_articles["text"])

    # Используем KMeans для кластеризации
    kmeans = KMeans(n_clusters=2, random_state=42)  # Два кластера для примера
    preprocessed_articles["cluster_id"] = kmeans.fit_predict(tfidf_matrix)

    return preprocessed_articles


def convert_to_json(clustered_articles):
    # Преобразуем DataFrame в JSON-массив
    return clustered_articles.to_dict(orient="records")