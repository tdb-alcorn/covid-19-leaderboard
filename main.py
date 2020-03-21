import csv

from flask import Flask

from datum import Datum, fitDatum, toHtml, htmlHeader
from util import asInt


app = Flask(__name__)


dataFile = 'covid_confirmed_usafacts.csv'
data = list()
with open(dataFile, newline='') as f:
    r = csv.reader(f)
    first = True
    for row in r:
        if first:
            first = False
        else:
            tr = list(map(asInt, row))
            data.append(tr)

# print(data)

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

# print(list(byFit(fitLast3Days(asDatum(ampleCases(data))))))
# print(list(res))
# print(len(res))

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

def page(title, data, best, worst):
    return '''
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>

            <h4>Last updated: 2020/03/20 6:39pm -0700

            <p>
                Do your part to slow the spread! Follow <a href='https://www.cdc.gov/coronavirus/2019-ncov/prepare/prevention.html'>CDC guidelines</a>.
            </p>

            <h2>Best</h>
            {best}

            <h2>Worst</h2>
            {worst}

            <h2>All</h2>
            <p>This table includes all counties reporting 10 or more confirmed cases.</p>
            {data}

            <p>
                Source: USAFacts <a href='https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/'>https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/</a>
            </p>

            <p>
                Doubling period is calculated using the fitted exponential growth rate over the last three days.
            </p>
        </body>
    </html>
    '''.format(title=title, data=data, best=best, worst=worst)

@app.route('/')
def main():
    return page("COVID-19 Leaderboard", table(res), table(res[:10]), table(reversed(res[-10:])))