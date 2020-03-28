#!/bin/bash

URL_CASES="https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
URL_DEATHS="https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv"

curl -O ${URL_CASES}
curl -O ${URL_DEATHS}