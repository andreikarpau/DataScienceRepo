import random

from mpl_toolkits.mplot3d import Axes3D
from scipy import misc
from sklearn.preprocessing import MinMaxScaler

from helper import FileHelper
import numpy as np
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt
import seaborn as sns


#Normalization
#----------------------------------------------------------
def min_max_norm(x):
    x = np.asarray(x)
    return (x - min(x)) / (max(x) - min(x))
#----------------------------------------------------------

ids, bedrooms, prices, latitudes, longitudes, bedroom_prices = FileHelper.get_geocoded_data()

data = np.column_stack([min_max_norm(latitudes), min_max_norm(longitudes), min_max_norm(prices)])

# Histogramms
#---------------------------------------------
# plt.hist(prices)
# plt.hist(bedrooms)
# plt.hist(bedroom_prices)
#---------------------------------------------

z = hac.linkage(data, method="single")

# Dendogram
#----------------------------------------------
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
hac.dendrogram(
    z,
    truncate_mode='lastp',
    p=120,
    leaf_rotation=90.,
    leaf_font_size=8.,
    show_contracted=True
)
plt.show()
print(z)

# Cutoff/Average per cluster
#----------------------------------------------
clusters = hac.fcluster(z, 0.11, 'distance')

avg_prices = []
clusters_size = []
cluster_name = []

for c in np.unique(clusters):
    avg_prices.append(np.mean(prices[clusters == c]))
    clusters_size.append(sum(clusters == c))
    cluster_name.append(c)

avg_prices = np.asarray(avg_prices)
clusters_size = np.asarray(clusters_size)
cluster_name = np.asarray(cluster_name)

clusters_relevant = 3 < clusters_size
relevant_items = []
for c in clusters:
    relevant_items.append(c in cluster_name[clusters_relevant])


# Apply Jitter
#-----------------------------------------------------------------------
disp_latitude = []
disp_longitude = []
random.seed(20)
jitter = 0.05
for i in range(0, len(latitudes)):
    disp_latitude.append(latitudes[i] + (random.random() - 0.5) * jitter)
    disp_longitude.append(longitudes[i] + (random.random() - 0.5) * jitter)

disp_latitude = np.asarray(disp_latitude)
disp_longitude = np.asarray(disp_longitude)
#
# disp_latitude = latitudes
# disp_longitude = longitudes


# 2d visualization
#------------------------------------------------------------------------
colors_list = ['red', 'blue', 'green', 'black', 'plum', 'orange', 'brown', 'palegreen', 'red', 'maroon', 'orchid', 'lightcoral', 'teal']

axes = plt.gca()
axes.set_xlim([14.1, 14.7])
axes.set_ylim([35.76, 36.15])

malta_img = misc.imread('data/malta_map.PNG')
plt.imshow(malta_img, zorder=0, extent=[14.1, 14.7, 35.76, 36.15])

for c_name in cluster_name[clusters_relevant]:
    c_items = clusters == c_name
    plt.scatter(disp_longitude[c_items], disp_latitude[c_items], s=10, label=c_name, color=colors_list[c_name])

plt.legend()
plt.show()

# 3d
#------------------------------------------------------------------------
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter(disp_longitude, disp_latitude, prices, c=clusters, s=1, cmap=plt.cm.get_cmap('hsv', max(clusters)))
# plt.show()

# Prices per cluster
#------------------------------------------------------------------------
plt.bar(cluster_name[clusters_relevant], avg_prices[clusters_relevant])
plt.xticks(cluster_name[clusters_relevant], cluster_name[clusters_relevant])
plt.show()

for i in range(len(clusters_relevant)):
    if clusters_relevant[i]:
        print("{0}: {1}; {2}".format(cluster_name[i], clusters_size[i], avg_prices[i]))


#print(avg_prices)
#print(clusters_size)
#print(clusters)
#print(len(clusters))