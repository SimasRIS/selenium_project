import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack # Naudojamas sujungti skirtingu tipu matricas


# Nurodome failo kelią
file_path = 'C:/Users/simas/PycharmProjects/selenium_project/data/processed/cleaned_review_comments.csv'
df = pd.read_csv(file_path)

def main():# Lietuviški stop words
    lithuanian_stop_words = [
        "ir", "su", "kad", "yra", "taip", "o", "ne", "į", "jis", "ji", "ar", "tai",
        "es", "buvo", "be", "kaip", "nuo", "prie", "už", "apie", "nors", "nei", "i",
        "uz", "bet"
    ]

    """
    1. DBSCAN klasterizacija pagal atsiliepimų turinį (temos)
    """
    # Paimame komentarų tekstus
    texts = df['Comment'].astype('str').values

    # Atlikame TF-IDF vektorizaciją
    tfidf = TfidfVectorizer(stop_words=lithuanian_stop_words,
                            max_features=3000,
                            min_df=2,
                            max_df=0.8)
    X = tfidf.fit_transform(texts)

    # DBSCAN grupavimas – parametrai eps ir min_samples koreguojami pagal duomenų savybes
    dbscan_text = DBSCAN(eps=0.5, min_samples=5)
    cluster_text = dbscan_text.fit_predict(X)
    df['Cluster_text'] = cluster_text

    print("\nClusters distribution by review contents")
    print(pd.Series(df['Cluster_text'].value_counts()))

    # Sumažiname dimensiją iki 2 naudojant PCA ir vizualizuoja rezultatus
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X.toarray())
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_text, cmap='plasma')
    plt.title('DBSCAN clusters by review contents')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.colorbar(scatter, label='Cluster number')
    plt.show()

    """
    2. DBSCAN klasterizacija pagal Star Score ir Comments
    """

    X_score = df['Star Score'].fillna(0).values.reshape(-1, 1)

    # Sujungiame Comments su Star Score
    X_combined = hstack([X, X_score])

    # Nomealizuojame duomenis
    scaler_2 = StandardScaler(with_mean=False)
    X_scaled = scaler_2.fit_transform(X_combined)

    # DBSCAN
    dbscan_combined = DBSCAN(eps=0.5, min_samples=5)
    cluster_combined = dbscan_combined.fit_predict(X_scaled)
    df['Cluster_combined'] = cluster_combined

    # Vizualizacija
    X_pca_combined = PCA(n_components=2).fit_transform(X_scaled.toarray())
    plt.figure(figsize=(8, 6))
    scatter_2 = plt.scatter(X_pca_combined[:, 0], X_pca_combined[:, 1],
                            c=cluster_combined, cmap='plasma')
    plt.title('DBSCAN clusters by Star Score and Review contents')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.colorbar(scatter_2, label='Cluster number')
    plt.show()

if __name__ == '__main__':
    main()




