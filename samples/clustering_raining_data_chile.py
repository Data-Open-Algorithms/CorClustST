from clust_st import CorClustST


def main():
    # download data

    # create distance matrix
    dist_matrix = None

    # create correlation matrix
    corr_matrix = None

    corclust_st = CorClustST(epsilon=1.7, rho=2.3)
    corclust_st.fit(dist_matrix, corr_matrix)
    labels = corclust_st.labels_

    # plots


if __name__ == "__main__":
    main()
