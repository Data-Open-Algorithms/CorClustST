import numpy as np


class CorClustST:
    def __init__(self, epsilon: float, rho: float, free_neigh_ratio: float = 0.5, min_cluster_size: int = 5) -> None:
        self.epsilon = epsilon
        self.rho = rho
        self.labels_ = None
        self.labels_correlations_ = None
        self.neigh_amount_initial_ = None
        self.st_neigh = None
        self.corr_matrix = None
        self.free_neigh_ratio = free_neigh_ratio
        self.min_cluster_size = min_cluster_size
        self.current_clustering_label = 0

    def step_1(self, distance_matrix, corr_matrix):
        self.corr_matrix = corr_matrix.values
        corr_neigh = self.corr_matrix > abs(self.rho)
        spat_neigh = distance_matrix < self.epsilon
        self.st_neigh = corr_neigh & spat_neigh
        # self.st_neigh = self.st_neigh - np.eye(corr_matrix.shape[0]) # ToDo : think about adding this line
        self.neigh_amount_initial_ = self.st_neigh.sum(axis=0)
        self.labels_ = np.ones(shape=(corr_matrix.shape[0],), dtype=int) * -1
        self.labels_correlations_ = np.zeros((corr_matrix.shape[0],))

    def step_3(self):
        free_neigh_amount = np.dot(self.st_neigh, (self.labels_ < 0) * 1)
        more_half_neigh_available = np.divide(free_neigh_amount, self.neigh_amount_initial_) > self.free_neigh_ratio
        next_more_neigh_candidate = (self.neigh_amount_initial_ * (self.labels_ < 0) * more_half_neigh_available).argmax()

        if self.st_neigh[next_more_neigh_candidate].sum() < self.min_cluster_size:
            return True

        new_best_cluster = (self.corr_matrix[next_more_neigh_candidate] > self.labels_correlations_) & self.st_neigh[
            next_more_neigh_candidate]

        self.labels_[new_best_cluster] = self.current_clustering_label

        new_cor = self.corr_matrix[next_more_neigh_candidate][new_best_cluster]
        self.labels_correlations_[new_best_cluster] = new_cor
        self.current_clustering_label = self.current_clustering_label + 1

    def step_5(self):
        for no_clus_point_it in np.where(self.labels_ == -1)[0]:
            neighs_with_cluster = self.st_neigh[no_clus_point_it] & (self.labels_ > 0)

            if neighs_with_cluster.sum() == 0:
                continue

            max_cor_neigh_with_cluster = self.corr_matrix[no_clus_point_it][neighs_with_cluster].argmax()
            max_cor_neigh_with_cluster_pos = np.where(neighs_with_cluster)[0][max_cor_neigh_with_cluster]
            cluster_to_assign = self.labels_[max_cor_neigh_with_cluster_pos]
            self.labels_[no_clus_point_it] = cluster_to_assign

    def fit(self, dist_matrix, corr_matrix):
        self.step_1(dist_matrix, corr_matrix)
        while True:
            if self.step_3():
                break
        self.step_5()

