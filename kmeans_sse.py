import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
import matplotlib


vectors = np.loadtxt("pc1-5_1dtja_5000.txt")


cluster_range = range(2, 401)
cluster_errors = []
for num_clusters in cluster_range:
    clusters = KMeans(num_clusters,init='k-means++').fit(vectors)
    cluster_errors.append( clusters.inertia_ )


clusters_df = pd.DataFrame.from_dict( {"num_clusters":cluster_range, "cluster_errors": cluster_errors})

font = {'family' : 'normal', 'size'   : 15}

plt.xlabel("k", fontsize=15)
plt.ylabel("Loss Function (SSE)", fontsize=15)
plt.grid(True)
plt.plot( clusters_df.num_clusters, clusters_df.cluster_errors, color = 'blue', linewidth=2)
plt.show()
fname = "1dtja_SSE.png"
#plt.savefig(fname, dpi=800,  orientation='landscape', transparent=True, bbox_inches=None, pad_inches=0.1)
