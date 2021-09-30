import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans

# dish_df = pd.read_csv('recipe_ingredient_One_hot_encoding.csv')
dish_df = pd.read_csv('recipe_ingredient_groups_One_hot_encoding.csv')
# dish_df = pd.read_csv('recipe_ingredient_groups_One_hot_encoding_v2.csv')


dish_df = dish_df.set_index('dish_ID')

n = 20
sse = []

kmeans_kwargs = {
    # "init": "random",
    "n_init": 100,
    "max_iter": 1000,
    "random_state": 42,
}

for k in range(1, n):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(dish_df.iloc[:, 1:])
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, n), sse)
plt.xticks(range(1, n))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

#膝蓋點在哪裡
kl = KneeLocator(
    range(1, n), sse, curve="convex", direction="decreasing"
)
k = kl.elbow
print('K = ', k)
               
kmeans = KMeans(n_clusters=k, **kmeans_kwargs).fit(dish_df.iloc[:, 1:])
results = kmeans.labels_
cluster_df = dish_df.iloc[:, 0:1] 
# cluster_df = dish_df
cluster_df['cluster'] = results

cluster_df.to_csv('cluster_results_100_1000_42.csv')
# results = pd.read_csv('cluster_results_100_1000_42.csv')

## PCA 降維 畫圖 觀察分群狀況

from sklearn.decomposition import PCA

X = dish_df.iloc[:, 1:]
y = cluster_df.iloc[:, -1]


X_2d = PCA(n_components = 2).fit_transform(X)

cluster_names = [0, 1, 2, 3, 4] # 5 clusters
target_ids = range(len(cluster_names))

from matplotlib import pyplot as plt
plt.figure(figsize=(6, 5))
colors = 'r', 'g', 'b', 'c', 'y'
for i, c, label in zip(target_ids, colors, cluster_names):
    plt.scatter(X_2d[y == i, 0], X_2d[y == i, 1], c=c, label=label)
plt.legend()
plt.show()

## t-sne 降維看分群狀況

# from sklearn.manifold import TSNE

# X = cluster_df.iloc[:, 1:] 
# y = cluster_df.iloc[:, -1]

# tsne = TSNE(n_components=2, random_state=0)

# X_2d = tsne.fit_transform(X)

# cluster_names = [0, 1, 2, 3, 4] # 5 clusters
# target_ids = range(len(cluster_names))

# plt.figure(figsize=(6, 5))
# colors = 'r', 'g', 'b', 'c', 'y'
# for i, c, label in zip(target_ids, colors, cluster_names):
#     plt.scatter(X_2d[y == i, 0], X_2d[y == i, 1], c=c, label=label)
# plt.legend()
# plt.show()