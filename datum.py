from collections import namedtuple
from util import expFit3, doublingTime


Datum = namedtuple('Datum', ['county', 'state', 'daym2', 'yesterday', 'today', 'fit', 'doubling_period', 'rank'])

def fitDatum(d):
    k = expFit3(d.daym2, d.yesterday, d.today)
    t = doublingTime(k)
    return d._replace(fit=k, doubling_period=t)

def toHtml(d):
    td = lambda s: '<td>' + s + '</td>'
    h = '<tr>'
    h += td('{:d}'.format(d.rank))
    h += td(d.county)
    h += td(d.state)
    h += td('{:d}'.format(d.yesterday))
    h += td('{:.2f}'.format(d.doubling_period))
    h += '</tr>'
    return h

columns = ['Rank', 'County', 'State', 'Confirmed cases', 'Doubling period (days)']
htmlHeader = '<tr>' + ''.join(['<th>{}</th>'.format(c) for c in columns]) + '</tr>'