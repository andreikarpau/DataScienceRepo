from sklearn.preprocessing import MinMaxScaler

from helper import FileHelper
import numpy as np
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt


#Normalization
#----------------------------------------------------------
def min_max_norm(x):
    x = np.asarray(x)
    return (x - min(x)) / (max(x) - min(x))
#----------------------------------------------------------

ids, bedrooms, prices, latitudes, longitudes, bedroom_prices = FileHelper.get_geocoded_data()

data = np.column_stack([min_max_norm(latitudes), min_max_norm(longitudes), min_max_norm(prices), min_max_norm(bedrooms)])

# Histogramms
#---------------------------------------------
# plt.hist(prices)
# plt.hist(bedrooms)
# plt.hist(bedroom_prices)
#---------------------------------------------

z = hac.linkage(data, method="single")

# Dendogram
#----------------------------------------------
# plt.figure(figsize=(25, 10))
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
# hac.dendrogram(
#     z,
#     truncate_mode='lastp',
#     p=120,
#     leaf_rotation=90.,
#     leaf_font_size=8.,
#     show_contracted=True
# )
# plt.show()
# print(z)

# Cutoff/Average per cluster
#----------------------------------------------
clusters = hac.fcluster(z, 0.18, 'distance')

avg_prices = {}
clusters_size = {}

for c in  np.unique(clusters):
    avg_prices[c] = np.mean(prices[clusters == c])
    clusters_size[c] = sum(clusters == c)

# Apply Jitter
plt.scatter(longitudes, latitudes, c=clusters, s=30, cmap=plt.cm.get_cmap('hsv', max(clusters)))
plt.colorbar()
plt.show()

print(avg_prices)
print(clusters_size)


print(clusters)
print(len(clusters))