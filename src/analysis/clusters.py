import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


file_path = 'C:/Users/simas/PycharmProjects/selenium_project/data/processed/cleaned_review_comments.csv'
df = pd.read_csv(file_path)

# Lietuviski stop words
lithuanian_stop_words = [
    "ir", "su", "kad", "yra", "taip", "o", "ne", "į", "jis", "ji", "ar", "tai",
    "es", "buvo", "be", "kaip", "nuo", "prie", "už", "apie", "nors", "nei", "i",
    "uz", "bet"
]

"""
1. Grupavimas pagal atsiliepimų turinį (temos).
"""
texts = df['Comment'].astype('str').values

tfidf = TfidfVectorizer(stop_words=lithuanian_stop_words)
X = tfidf.fit_transform(texts)

# Grupavimas

dbscan_text = DBSCAN(eps=0.5, min_samples=5)
cluster_text = dbscan_text.fit_predict(X)
df['Cluster_text'] = cluster_text

print("\nClusters distribution by review contents")
print(pd.Series(df['Cluster_text'].value_counts()))


# Vizua;izacija naudojant PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X.toarray())

plt.figure(figsize=(8, 6))
scratter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_text, cmap='plasma')
plt.title('DBSCAN clusters by review contents')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.colorbar(scratter, label='Cluster number')
plt.show()

"""
2. Klasterizavimas pagal reitingus ir teksta
"""
# Pasirenkame stulpelius
X_numeric = df[['Star Score', "Comment"]].values

# Normalizuojame duomenis
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_numeric)

# DBSCAN klasterizavima
dbscan_numeric = DBSCAN(eps=0.5, min_samples=5)
cluster_numeric = dbscan_numeric.fit_predict(X_scaled)
df['Cluster_numeric'] = cluster_numeric

print("\nClusters distribution by raiting review contents")
print(pd.Series(df['Cluster_numeric'].value_counts()))

pca_numeric = PCA(n_components=2)
X_numeric_pca = pca_numeric.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
scratter2 = plt.scatter(X_numeric_pca[:, 0], X_numeric_pca[:, 1],c=cluster_numeric ,cmap='plasma')
plt.title('PCA clusters by raiting and review contents')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.colorbar(scratter2, label='Cluster number')
plt.show()


