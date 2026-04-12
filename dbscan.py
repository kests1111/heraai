import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(r"C:\Users\soldierofgabe\Downloads\irises.csv")
df1 = df.drop(columns = ['Species'])
print(df)

X = df1
scaler = StandardScaler()
X = scaler.fit_transform(X)
# дб скан----------------------------------------------------------------------
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))
 

def region_query(X, point_idx, eps):
    neighbors = []
    for i in range(len(X)):
        if euclidean_distance(X[point_idx], X[i]) <= eps:
            neighbors.append(i)
    return neighbors

def expand_cluster(X, labels, point_idx, neighbors, cluster_id, eps, min_samples):
    labels[point_idx] = cluster_id

    i = 0
    while i < len(neighbors):
        neighbor_idx = neighbors[i]

        if labels[neighbor_idx] == -1:  
            labels[neighbor_idx] = cluster_id

        if labels[neighbor_idx] == 0:  
            labels[neighbor_idx] = cluster_id
            new_neighbors = region_query(X, neighbor_idx, eps)

            if len(new_neighbors) >= min_samples:
                neighbors += new_neighbors

        i += 1

def dbscan(X, eps=0.5, min_samples=5):
    n = len(X)
    labels = np.zeros(n) 
    cluster_id = 0

    for i in range(n):
        if labels[i] != 0:
            continue

        neighbors = region_query(X, i, eps)

        if len(neighbors) < min_samples:
            labels[i] = -1 
        else:
            cluster_id += 1
            expand_cluster(X, labels, i, neighbors, cluster_id, eps, min_samples)

    return labels

labels = dbscan(X, eps=0.7, min_samples=5)
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

# --- KMEANS ПОСЛЕ DBSCAN ---

core_mask = labels != -1
X_core = X[core_mask]

# количество кластеров из DBSCAN (без шума)
k = len(set(labels)) - (1 if -1 in labels else 0)

kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X_core)

# предсказание для всех точек
final_labels = kmeans.predict(X)

# --- ACCURACY ---

le = LabelEncoder()
true_labels = le.fit_transform(df['Species'])

predicted_labels = np.full_like(true_labels, -1)

for cluster in set(final_labels):
    indices = np.where(final_labels == cluster)[0]
    true_cluster_labels = true_labels[indices]

    most_common = np.bincount(true_cluster_labels).argmax()
    predicted_labels[indices] = most_common

accuracy = np.mean(predicted_labels == true_labels)

print("Final Accuracy (DBSCAN + KMeans):", accuracy)
# аккьюраси---------------------------------------------------------------------------
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
true_labels = le.fit_transform(df['Species'])

predicted_labels = np.full_like(true_labels, -1)

for cluster in set(labels):
    if cluster == -1:
        continue

    indices = np.where(labels == cluster)[0]
    true_cluster_labels = true_labels[indices]

    most_common = np.bincount(true_cluster_labels).argmax()
    predicted_labels[indices] = most_common


mask = labels != -1
accuracy_clusters = np.mean(predicted_labels[mask] == true_labels[mask])


accuracy_full = np.mean(predicted_labels == true_labels)

print("Accuracy (clusters only):", accuracy_clusters)
print("Accuracy (full):", accuracy_full)

print("Total:", len(labels))
print("Clustered:", np.sum(labels != -1))
print("Noise:", np.sum(labels == -1))