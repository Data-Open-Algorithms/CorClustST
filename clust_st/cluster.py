class CorClustST:
    def __init__(self, epsilon: float, rho: float) -> None:
        self.epsilon = epsilon
        self.rho = rho
        self.labels_ = None

    def fit(self, dist_matrix, corr_matrix):
        pass