# COVID-19 Leaderboard

## Build


1. Make a python3 virtual env in the project directory `python3 -m venv env`
2. Activate it `. ./env/bin/activate`
3. `pip install -r requirements.txt`
4. Install the [Heroku command line tools](https://devcenter.heroku.com/articles/heroku-cli) (Linux: `curl https://cli-assets.heroku.com/install.sh | sh`)
5. Run `heroku local`
6. Navigate your browser to `localhost:5000`

## Ideas

- do 3-6 days ago for comparison
- automate pulling new data (currently manually download CSV once per day)
- number of ICUs / ventilators and current utilisation
- number of hospitals in the county
- show county population
- group counties into cities/metros
- sort by any column
- deaths, deaths doubling period
- show graph
- mix in local news headlines from the best and worst counties to unlock insights
- leaderboard for US states
- show history datapoints for each county
    - allow grouping of multiple counties for above feature
- add trends and interactive past rankings
- add international data, leaderboard for nations
- last 3 days, last 7 days
- add a map view
- median income of county
