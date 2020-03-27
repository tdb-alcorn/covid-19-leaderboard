import math
import numpy as np


def least_squares_linear_fit(x, y):
    '''
    Assumes series of xs and ys has the same length.
    Computes fit as
    | A B |    | D |
    | B C | .* | E |
    following the least squares fitting formula at https://mathworld.wolfram.com/LeastSquaresFitting.html
    '''
    n = x.shape[0]
    sum_x = np.sum(x)
    sum_x2 = np.sum(np.square(x))
    sum_y = np.sum(y)
    sum_xy = np.sum(np.dot(x, y))

    L = np.array([
        [n, sum_x],
        [sum_x, sum_x2],
        ])
    R = np.array([[sum_y, sum_xy]]).T
    L_inv = np.linalg.inv(L)
    fit = np.matmul(L_inv, R)
    
    c = fit[0][0]
    m = fit[1][0]
    return c, m

def exp_fit(x, y):
    c, m = least_squares_linear_fit(np.array(x), np.log(np.array(y)+1e-10))
    A = np.exp(c)
    k = m
    return A, k

def asInt(x):
    try:
        return int(x)
    except ValueError:
        return x

def mean_growth_rate(X, Y):
    dY = np.diff(Y)
    dX = np.diff(X)
    dYdX = dY/dX
    nz = Y[1:].nonzero()[0]
    if nz.size == 0:
        return 0
    k = dYdX[nz] / Y[1:][nz]
    return np.mean(k)

# def geometricMean(x, y):
#     if x < 0 or y < 0:
#         return 0
#     return math.sqrt(x*y)

# def expFit3(a, b, c):
#     k0 = computeGrowthRate(a, b)
#     k1 = computeGrowthRate(b, c)
#     return geometricMean(k0, k1)

def doubling_period(k):
    if k == 0:
        return math.inf
    return math.log(2)/k
