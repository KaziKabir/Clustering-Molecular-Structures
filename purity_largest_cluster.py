
maximum = 0
with open("clusters_kmeans_1dtja_5000.txt", "r") as f:
    array = []
    for line in f:
        y = line.split()
        k = len(y)
        array.append(k)
        if maximum < k:
            x = y
            maximum = k

#print(array.index(maximum))

with open("1dtja_rmsd_5000.txt", "r") as ff:
    rmsd_array = [float(line.split()[0]) for line in ff]


top_cluster_rmsd = []

for val in x:
    k= int(val)
    top_cluster_rmsd.append(rmsd_array[k])


dist_thresh = 2.0 # rmsd threshold with respect to native for 1dtj(A)

c1 = 0
for v1 in top_cluster_rmsd:
    if v1 <= dist_thresh:
        c1 = c1 + 1


print("Purity Percentage")
print(c1*100/len(top_cluster_rmsd))
