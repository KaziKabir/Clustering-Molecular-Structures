import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans


vectors = np.loadtxt("pc1-5_1dtja_5000.txt")




num_clusters = 75 # optimal-k
clusters = KMeans(num_clusters,init='k-means++').fit(vectors)

Y = clusters.labels_

for i in range(max(Y)+1):
    xy = [index for index, value in enumerate(Y) if value == i]
    for v in xy:
        print(v, end=" ")
    print()
