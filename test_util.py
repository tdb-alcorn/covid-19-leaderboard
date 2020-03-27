import unittest
import numpy as np

from util import *


class TestFit(unittest.TestCase):
    def test_least_squares_linear_fit(self):
        for i in range(10):
            m = np.random.random() * 100 - 50
            c = np.random.random() * 100 - 50
            xs = np.array([1, 2, 3])
            ys = m * xs + c
            fit_c, fit_m = least_squares_linear_fit(xs, ys)
            self.assertAlmostEquals(m, fit_m)
            self.assertAlmostEquals(c, fit_c)

    def test_exp_fit(self):
        for i in range(10):
            A = np.random.random() * 2
            k = np.random.random() * 2 - 1
            xs = np.array([0, 1, 2])
            ys = A * np.exp(k * xs)
            fit_A, fit_k = exp_fit(xs, ys)
            print(A, k, ys, fit_A, fit_k)
            self.assertAlmostEquals(k, fit_k)
            self.assertAlmostEquals(A, fit_A)
    

if __name__ == '__main__':
    unittest.main()