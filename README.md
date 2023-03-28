# Delaware North take-home assignment
This repository houses my submission for the Delaware North take-home assignment. The code should be runnable by following the instructions below.

## How to run:

This guide assumes you are on mac and have python3 installed. This solution was developed on Python 3.7.3 and has not been tested in other languages.

1. Clone the repository
1. Create a virtualenv if you'd like: `python3 -m venv my-venv`
  1. If you did this step, activate it! `source my-venv/bin/activate`
1. Install the required libraries: `pip install -r requirements.txt`
1. Update the dataset* if desired. This can be exported via `csv` [here](https://healthdata.gov/dataset/COVID-19-Diagnostic-Laboratory-Testing-PCR-Testing/j8mb-icvb/explore/query/SELECT%0A%20%20%60state%60%2C%0A%20%20%60state_name%60%2C%0A%20%20%60state_fips%60%2C%0A%20%20%60fema_region%60%2C%0A%20%20%60overall_outcome%60%2C%0A%20%20%60date%60%2C%0A%20%20%60new_results_reported%60%2C%0A%20%20%60total_results_reported%60%2C%0A%20%20%60geocoded_state%60/page/filter). Once this is completed, replace the file in `data/Dataset.csv`. Please download all columns to ensure best results.
1. Run the code: `python main.py`. This will produce the results for all three sections as well as a figure in `figures/rolling_averages.png`!

\*I did consider pulling the dataset live in the code. More on this in the Enhancements section.

## Details for each calculation

### Total number of PCR tests performed as of yesterday in the United States.

Notes/assumptions for this calculation:

* Everything in the dataset is considered "in the United States". So, I've kept in US Virgin Islands, Guam, etc.
* I did not specifically exclude data from today as I did not see it in the dataset. If the dataset ever includes data from today (the most recent), that would be included.
* `total_results_reported` will never decrease. For performance, I've decided to sort the dataset by date and pick the latest result as opposed to calculating the maximum `total_results_reported` value for each state.

### The 7-day rolling average number of new cases per day for the last 30 days

Notes/assumptions for this calculation:

* The past 2-3 days did not seem to have any data. I've left them in the calculation as a 0 which significantly lowers the rolling average for those days. I'm not sure if this is a recency issue (there's never data for the past 2-3 days) or there was a one-off issue. This impacts the positivity rate calculation as well.
* I've rounded averages to two decimal places.
* The past 30 days does not include today.

### The 10 states with the highest test positivity rate (positive tests / tests performed) for tests performed in the last 30 days.

* Iowa does not seem to be reporting Negative/Inconclusive tests anymore, so they are showing as a 100% positivity rate. I've decided not to exclude this from the results.
* I've rounded averages to two decimal places.
* The past 30 days does not include today.

## Enhancements

Here's a short list of enhancements I would make with more time. They're listed roughly in priority order

* Fetch the data live. I started to do this using `sodapy`, but ran into a rate limit. I considered getting an application token, but ultimately decided not to given that I wasn't sure how long that would take. Here's a bit of sample code to fetch data from the past 30 days (this would make the code much faster):
```python
import pandas as pd
from sodapy import Socrata
import datetime


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("healthdata.gov", None)

now = datetime.datetime.now()
thirty = now - datetime.timedelta(days=30)
datestr = f'{thirty.year}-{thirty.month}-{thirty.day}' 

results = client.get("j8mb-icvb", where=f'date >= "{datestr}"', limit=7000)
df = pd.DataFrame.from_records(results)
```
* Include the new case count for individual days in the plot for part two. I think seeing these two metrics next to each other would be interesting!
* Clean, validate, and sanitize the data much more thoroughly. Upon initial inspection and working with the data, I found that it was mostly clean and sane, but in a production setting, this step would be imperative.
* Better pandas <> date querying. I used the `datestr` method you see a few times in `calculations.py` at the onset, then found it worked and didn't want to spend the time to replace it. I'm sure there's a better way, but with the simple date format in the dataset, this doesn't seem like a big concern at the moment.
  * In general, I could be cleaner with dates as well. I would like to be clearer and cleaner with my intentions using dates (for example, with timezones and timestamps) in a realistic/production environment.
* Use a python queue instead of an array for rolling averages. Given that it only ever gets to be of length 7, I don't think this is a very big deal.
