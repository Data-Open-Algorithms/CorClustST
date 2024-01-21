from scipy.stats import rankdata
import numpy as np

class CorClustST:
    def __init__(self, epsilon: float, rho: float) -> None:
        self.epsilon = epsilon
        self.rho = rho
        self.labels_ = None
        self.neigh_amount_initial_ = None

    def step_0(self, distance_matrix, corr_matrix):
        corr_matrix = corr_matrix.values
        corr_neigh = corr_matrix > abs(self.rho)
        spat_neigh = distance_matrix < self.epsilon
        st_neigh = corr_neigh & spat_neigh
        self.neigh_amount_initial_ = st_neigh.sum(axis=0)
        self.labels_ = np.ones((corr_matrix.shape[0],)) * -1

    def step_1(self, distance_matrix, corr_matrix):
        corr_matrix = corr_matrix.values
        corr_neigh = corr_matrix > abs(self.rho)
        spat_neigh = distance_matrix < self.epsilon
        st_neigh = corr_neigh & spat_neigh
        neigh_amount = np.dot(st_neigh, (self.labels_ < 0)*1)

        more_half_neigh_available = np.divide(neigh_amount, self.neigh_amount_initial_) > 0.5
        # for candidate

    def fit(self, dist_matrix, corr_matrix):
        self.step_0(dist_matrix, corr_matrix)
        self.step_1(dist_matrix, corr_matrix)
