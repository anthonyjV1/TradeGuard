from sklearn.decomposition import PCA
import pandas as pd

def apply_pca(X_scaled: pd.DataFrame, n_components: int = 2):
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)
    pca_df = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(n_components)])
    return pca_df, pca
