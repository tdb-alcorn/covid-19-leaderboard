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

def as_int(x):
    try:
        return int(x)
    except ValueError:
        return x

def drop_columns(row, indices):
    return [row[i] for i in range(len(row)) if i not in indices]

def mean_growth_rate(X, Y, uncertainty_delta=0.1):
    dY = np.diff(Y)
    dX = np.diff(X)
    dYdX = dY/dX
    nz = Y[1:].nonzero()[0]
    if nz.size == 0:
        return 0
    Y_nz = Y[1:][nz]
    dYdX_nz = dYdX[nz]
    k = dYdX_nz / Y_nz
    dU = 2 + uncertainty_delta * dYdX_nz
    low = (dYdX_nz - dU) / Y_nz
    high = (dYdX_nz + dU) / Y_nz
    return Uncertain(np.mean(k), np.mean(low), np.mean(high))

def doubling_period(k):
    if k == 0:
        return math.inf
    return math.log(2)/k


def format_uncertain_days(x):
    '''x must be an instance of Uncertain'''
    if x.value > 100:
        return "months"
    else:
        uncertainty = "{:.2g}".format(x.uncertainty)
        if x.uncertainty > 100:
            uncertainty = "months"
        return "{:.2g} ± {:s}".format(x.value, uncertainty)


class Uncertain:
    def __init__(self, value, low, high):
        self.value = value
        if low > high:
            self.low = high
            self.high = low
        else:
            self.low = low
            self.high = high
        if self.value < self.low or self.value > self.high:
            raise ValueError("{value} must be between low={low} and high={high}".format(
            value=value, low=low, high=high))
        self.uncertainty = np.mean(np.abs([self.value - self.low, self.high-self.value]))
    
    def apply(self, f):
        return Uncertain(f(self.value), f(self.low), f(self.high))
    
    def __str__(self):
        return "{:g} ({:g} -> {:g})".format(self.value, self.low, self.high)
    
    def __repr__(self):
        return self.__str__()