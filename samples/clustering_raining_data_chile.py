import unittest
import numpy as np
from clust_st import CorClustST

expected_clusters = [
    '5100006',
    '5427008',
    '360011',
    '340031',
    '10312001',
    '4502005',
    '8367001',
    '1020017',
    '4554003',
    '3815004',
    '10350001',
    '3431004',
    '10904005',
    '1730020',
    '450005',
    '2101003',
    '520006'
]

def main():
    # download data

    # create distance matrix
    dist_matrix = None

    # create correlation matrix
    corr_matrix = None

    corclust_st = CorClustST(epsilon=1.7, rho=2.3)
    corclust_st.fit(dist_matrix, corr_matrix)
    cluster_centers = corclust_st.cluster_centers_
    # labels = corclust_st.labels_
    expected_center = np.array(expected_clusters)
    np.testing.assert_array_equal(expected_center, cluster_centers.index)
    # plots


if __name__ == "__main__":
    main()
