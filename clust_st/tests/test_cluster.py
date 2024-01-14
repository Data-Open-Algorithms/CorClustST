import unittest
from clust_st import CorClustST

class TestClusterMethods(unittest.TestCase):
    def test_init(self):
        rho = 2.3
        epsilon = 1.7
        corclust_st = CorClustST(epsilon, rho)
        self.assertEqual(corclust_st.rho, rho)
        self.assertEqual(corclust_st.epsilon, epsilon)  