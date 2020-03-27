from collections import namedtuple

import numpy as np

from util import mean_growth_rate, doubling_period


Datum = namedtuple('Datum', ['county', 'state', 
    'series', 'current', 'sum',
    'fit', 'doubling_period', 'rank'])

def fitDatum(d):
    x = np.array([0, 1, 2, 3])
    cum_sum = sum(d.series[:-4])
    bias = 0.1*np.exp(0.1*x)
    y = np.cumsum(np.array(d.series[-4:])) + cum_sum + bias
    # A, k = exp_fit(x, y)
    # k = expFit3(*d.series[-3:])
    k = mean_growth_rate(x, y)
    t = doubling_period(k)
    return d._replace(fit=k, doubling_period=t)

def toHtml(d):
    td = lambda s: '<td>' + s + '</td>'
    h = '<tr>'
    h += td('{:d}'.format(d.rank))
    h += td(d.county)
    h += td(d.state)
    h += td('{:d}'.format(d.sum))
    h += td('{:d}'.format(d.current))
    h += td('{:.2g}'.format(d.doubling_period))
    h += '</tr>'
    return h

columns = ['Rank', 'County', 'State', 'Deaths (total)', 'Deaths (change)', 'Doubling period (days)']
htmlHeader = '<tr>' + ''.join(['<th>{}</th>'.format(c) for c in columns]) + '</tr>'