from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

def run_kmeans(X_pca: pd.DataFrame, n_clusters: int = 3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_pca)
    silhouette = silhouette_score(X_pca, labels)
    return labels, kmeans, silhouette