import os
import datetime
import csv

from flask import Flask

from datum import Datum, fitDatum, toHtml, htmlHeader
from util import asInt


app = Flask(__name__)


data_file = 'covid_confirmed_usafacts.csv'
last_updated = datetime.datetime.fromtimestamp(os.path.getmtime(data_file))
data = list()
with open(data_file, newline='') as f:
    r = csv.reader(f)
    first = True
    for row in r:
        if first:
            first = False
        else:
            tr = list(map(asInt, row))
            data.append(tr)


# transforms
def asDatum(data):
    return map(lambda r: Datum(r[1], r[2], *r[-3:], 0, 0), data)

def fitLast3Days(data):
    return map(fitDatum, data)

# filters
def ampleCases(data):
    return filter(lambda d: d.yesterday > 10, data)

def hasGrowth(data):
    return filter(lambda d: d.fit > 0, data)

# sorts

def byFit(data):
    return sorted(data, key=lambda d: d.fit)

pipeline = [
    asDatum,
    ampleCases,
    fitLast3Days,
    hasGrowth,
    byFit,
]

res = data
for stage in pipeline:
    res = stage(res)


def table(data):
    t = '<table>'

    t += '<thead>'
    t += htmlHeader
    t += '</thead>'

    t += '<tbody>'
    for d in data:
        t += toHtml(d)
    t += '</tbody>'

    t += '</table>'

    return t

html = None
with open('index.html') as f:
    html = f.read()

css = ''
with open('Skeleton-2.0.4/css/normalize.css') as f:
    css += f.read()
with open('Skeleton-2.0.4/css/skeleton.css') as f:
    css += f.read()

def page(html, css, title, data, best, worst, last_updated):
    return html.format(stylesheet=css, title=title, data=data, best=best, worst=worst,
               last_updated=last_updated)

@app.route('/')
def main():
    return page(html, css, "COVID-19 Leaderboard", table(res), table(res[:10]),
                table(reversed(res[-10:])), last_updated.ctime())