__author__ = 'askofen'

from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
from sklearn import preprocessing
import numpy as np
import scipy as sp

data = sp.genfromtxt("../../Data/seeds.tsv", delimiter="\t")
data = data[:,range(0,7)]

labels = sp.genfromtxt("../../Data/seeds.tsv", delimiter="\t", dtype=str)
labels = labels[:,7]

def distance(p0, p1): return np.sum((p0-p1)**2)

def nn_classify(training_set, training_labels, new_example):
    dists = np.array([distance(t, new_example) for t in training_set])
    nearest = dists.argmin()
    return training_labels[nearest]

def plot_data(data_to_plot_x, data_to_plot_y):
    for i in range(0, labels.size):
        if (labels[i] == 'Kama'):
            m = '>'
            c = 'g'
        elif labels[i] == 'Rosa':
            m = 'o'
            c = 'r'
        elif labels[i] == 'Canadian':
            m = 'x'
            c = 'b'

        plt.scatter(data_to_plot_x[i], data_to_plot_y[i], marker=m, c=c)

#plt.show()

ndata = sp.ones(data.shape)

for i in range(0, data.shape[1]):
    mean = data[:,i].mean(axis=0)
    std = data[:,i].std(axis=0)
    ndata[:,i] = (data[:,i].copy() - mean) / std


plot_data(ndata[:,0], ndata[:,1])


zScaler = preprocessing.StandardScaler().fit(data.copy())
zData = zScaler.transform(data.copy())