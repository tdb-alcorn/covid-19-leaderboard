import math


def asInt(x):
    try:
        return int(x)
    except ValueError:
        return x

def computeGrowthRate(a, b):
    if b == 0:
        return 0
    if a < 1:
        return math.log(b/(a+1))
    return math.log(b/a)

def geometricMean(x, y):
    if x < 0 or y < 0:
        return 0
    return math.sqrt(x*y)

def expFit3(a, b, c):
    k0 = computeGrowthRate(a, b)
    k1 = computeGrowthRate(b, c)
    return geometricMean(k0, k1)

def doublingTime(k):
    if k == 0:
        return math.inf
    return math.log(2)/k
