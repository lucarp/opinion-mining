import sys
from sklearn import metrics
import pandas as pd
import numpy as np

X = pd.read_csv(sys.argv[1], header=0, index_col=0)
X = np.matrix(X)
print(X.shape)
labels = pd.read_csv(sys.argv[2], header=0, index_col=0)
labels = np.ravel(np.matrix(labels))
print(labels.shape)

input()

print("compute silhouette_score...")
sc = metrics.silhouette_score(X, labels)
print("compute silhouette_score (cosine)...")
sc_cos = metrics.silhouette_score(X, labels, metric='cosine')
print("compute calinski_harabaz_score...")
chi = metrics.calinski_harabaz_score(X, labels)
print("compute davies_bouldin_score...")
dbi = metrics.davies_bouldin_score(X, labels)

print("SC       = {}".format(sc))
print("SC (cos) = {}".format(sc_cos))
print("CHI      = {}".format(chi))
print("DBI      = {}".format(dbi))
