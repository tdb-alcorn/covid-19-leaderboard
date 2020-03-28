import os
import datetime
import csv

from flask import Flask

from datum import to_html, html_header, row_to_datum, fit_datum
from util import as_int, drop_columns


app = Flask(__name__)


data_file_cases = 'covid_confirmed_usafacts.csv'
data_file_deaths = 'covid_deaths_usafacts.csv'
last_updated = datetime.datetime.fromtimestamp(os.path.getmtime(data_file_deaths))

def read_data_file(data_file: str):
    data = list()
    with open(data_file, newline='', encoding='utf-8-sig') as f:
        r = csv.reader(f)
        first = True
        empty_columns = None
        for row in r:
            if first:
                first = False
                empty_columns = [i for i in range(len(row)) if row[i] == '']
            else:
                tr = list(map(as_int, drop_columns(row, empty_columns)))
                data.append(tr)
    return data

# data_cases = read_data_file(data_file_cases)
data_deaths = read_data_file(data_file_deaths)
data = data_deaths

# transforms
def as_datum(data):
    return map(row_to_datum, data)

def fit_last_3_days(data):
    return map(fit_datum, data)

def with_rank(data):
    return [data[i]._replace(rank=i+1) for i in range(len(data))]


# filters
def has_deaths(data):
    return filter(lambda d: d.sum > 1, data)

def has_growth(data):
    return filter(lambda d: d.fit.value > 0, data)

# sorts

def by_doubling_period(data):
    return sorted(data, key=lambda d: d.doubling_period.high, reverse=True)

pipeline = [
    as_datum,
    has_deaths,
    fit_last_3_days,
    # has_growth,
    by_doubling_period,
    with_rank,
]

res = data
for stage in pipeline:
    res = stage(res)


def table(data):
    t = '<table>'

    t += '<thead>'
    t += html_header
    t += '</thead>'

    t += '<tbody>'
    for d in data:
        t += to_html(d)
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