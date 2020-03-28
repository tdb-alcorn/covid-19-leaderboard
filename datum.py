from collections import namedtuple

import numpy as np

from util import mean_growth_rate, doubling_period, format_uncertain_days


Datum = namedtuple('Datum', ['county', 'state', 
    'series', 'current', 'sum',
    'fit', 'doubling_period',
    'rank'])

def row_to_datum(r):
    try:
        return Datum(r[1], r[2], r[4:], r[-1], sum(r[4:]), 0, 0, 0)
    except TypeError as e:
        print(r)
        raise e

def fit_datum(d):
    x = np.array([0, 1, 2, 3])
    cum_sum = sum(d.series[:-4])
    bias = 0.1*np.exp(0.1*x)
    y = np.cumsum(np.array(d.series[-4:])) + cum_sum + bias
    k = mean_growth_rate(x, y)
    # t = doubling_period(k)
    t = k.apply(lambda x: x if x > 0 else 1e-10).apply(doubling_period)
    dn = d._replace(fit=k, doubling_period=t)
    # if dn.county == "King County" and dn.state == "WA":
    #     print(dn)
    return dn

def to_html(d):
    td = lambda s: '<td>' + s + '</td>'
    h = '<tr>'
    h += td('{:d}'.format(d.rank))
    h += td(d.county)
    h += td(d.state)
    h += td('{:d}'.format(d.sum))
    h += td('{:d}'.format(d.current))
    # h += td('{:.2g} ± {:.2g}'.format(d.doubling_period, d.doubling_period_uncertainty))
    h += td(format_uncertain_days(d.doubling_period))
    h += '</tr>'
    return h

columns = ['Rank', 'County', 'State', 'Deaths (total)', 'Deaths (change)', 'Doubling period (days)']
html_header = '<tr>' + ''.join(['<th>{}</th>'.format(c) for c in columns]) + '</tr>'