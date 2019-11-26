Sequence of Execution of the source code files:

  1. Execute extract_CA.py (this step can be skipped if we don't have the pdb file. In that case, we start from 2 with the
     onedtja_CA_5000.txt file having the CA coordinates of the structures)

  2. Execute featurizer.py

  3. Execute kmeans_sse.py to find the optimal k

  4. Execute kmeans.py with the optimal value for k
     and store the output file from the console in the text file. Type the following from the console:
     python kmeans.py > clusters_kmeans_1dtja_5000.txt

  5. Execute extract_CA_native.py

  6. Execute compute_rmsd.py

  7. Execute purity_largest_cluster.py (this file reads cluster output file clusters_kmeans_1dtja_5000.txt)

  Note: Before repeating the whole sequence, delete all the text files except ReadMe.txt (and also except onedtja_CA_5000.txt if there is 
        no pdb file)
