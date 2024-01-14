class CorClustST:
    def __init__(self, epsilon: float, rho: float) -> None:
        self.epsilon = epsilon
        self.rho = rho
        self.labels_ = None

    def step_1(self, distance_matrix, corr_matrix):
        pass

    def fit(self, dist_matrix, corr_matrix):
        self.step_1(dist_matrix, corr_matrix)
