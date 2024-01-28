from scipy.stats import rankdata
import numpy as np

class CorClustST:
    def __init__(self, epsilon: float, rho: float, neigh_ratio: float = 0.5) -> None:
        self.epsilon = epsilon
        self.rho = rho
        self.neigh_ratio = neigh_ratio
        self.labels = None
        self._corr_matrix = None
        self._st_neigh = None
        self._neigh_amount_initial = None
        self._corr_to_cluster = None

    def _get_st_neighbors(self, dist_matrix):
        corr_neigh = self._corr_matrix > abs(self.rho)
        spat_neigh = dist_matrix < self.epsilon
        return corr_neigh & spat_neigh

    def _get_sorted_st_neigh_idx(self, st_neigh):
        self._neigh_amount_initial = st_neigh.sum(axis = 0) - 1 # Amount of neighbors
        return np.flip(np.argsort(self._neigh_amount_initial))

    def _assign_neighbors_cluster(self, point, clust_idx):
        self.labels[self._st_neigh[:, point]] = clust_idx
        self._corr_to_cluster[np.where(self._st_neigh[:, point])[0]] = self._corr_matrix[np.where(self._st_neigh[:, point])[0], point]

    def _assign_neighbors_not_assinged(self, point, clust_idx):
        not_assigned = (self.labels == -1) & self._st_neigh[:, point]
        self.labels[not_assigned] = clust_idx
        self._corr_to_cluster[np.where(self._st_neigh[:, point])[0]] = self._corr_matrix[np.where(self._st_neigh[:, point])[0], point]

    def _override_assigned_by_corr(self, point, clust_idx):
        assigned = (self.labels != -1) & self._st_neigh[:, point]
        assigned_idx = np.where(assigned)[0]
        for idx in assigned_idx:
            if self._corr_matrix[point, idx] > self._corr_to_cluster[idx]:
                self.labels[idx] = clust_idx
                self._corr_to_cluster[idx] = self._corr_matrix[point, idx] 

    def _init_fit(self, corr_matrix):
        self._corr_matrix = corr_matrix
        self.labels = np.full(corr_matrix.shape[0], -1)
        self._corr_to_cluster = np.full(corr_matrix.shape[0], 0)

    def fit(self, dist_matrix, corr_matrix):
        self._init_fit(corr_matrix)
        self._st_neigh = self._get_st_neighbors(dist_matrix) # Neighbor matrix
        sorted_st_neigh_idx = self._get_sorted_st_neigh_idx(self._st_neigh)
        clust_idx = 0
        self._assign_neighbors_cluster(sorted_st_neigh_idx[0], clust_idx)
        for i in range(1, len(sorted_st_neigh_idx)):
            point = sorted_st_neigh_idx[i]
            if self.labels[point] != -1:
                continue
            assigned_neigh = (self.labels[self._st_neigh[:, point]] != -1).sum() - 1
            if assigned_neigh / self._neigh_amount_initial[point] > 0.5:
                continue
            if self._neigh_amount_initial[point] - assigned_neigh < 5:
                continue
            clust_idx += 1 # Create new cluster
            self._override_assigned_by_corr(point, clust_idx)
            self._assign_neighbors_not_assinged(point, clust_idx)
