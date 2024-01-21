from scipy.stats import rankdata
import numpy as np

class CorClustST:
    def __init__(self, epsilon: float, rho: float, free_neigh_ratio: float = 0.5) -> None:
        self.epsilon = epsilon
        self.rho = rho
        self.labels_ = None
        self.neigh_amount_initial_ = None
        self.st_neigh = None
        self.free_neigh_ratio = free_neigh_ratio

    def step_0(self, distance_matrix, corr_matrix):
        corr_matrix = corr_matrix.values
        corr_neigh = corr_matrix > abs(self.rho)
        spat_neigh = distance_matrix < self.epsilon
        self.st_neigh = corr_neigh & spat_neigh

        # self.st_neigh = self.st_neigh - np.eye(corr_matrix.shape[0]) # ToDo : think about adding this line

        self.neigh_amount_initial_ = self.st_neigh.sum(axis=0)
        self.labels_ = np.ones((corr_matrix.shape[0],)) * -1

    def step_1(self, distance_matrix, corr_matrix):
        free_neigh_amount = np.dot(self.st_neigh, (self.labels_ < 0)*1)
        more_half_neigh_available = np.divide(free_neigh_amount, self.neigh_amount_initial_) > self.free_neigh_ratio




    def fit(self, dist_matrix, corr_matrix):
        self.step_0(dist_matrix, corr_matrix)
        self.step_1(dist_matrix, corr_matrix)
