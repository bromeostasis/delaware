import datetime
import pandas as pd
import matplotlib.pyplot as plt

from calculations.calculations import *
from sodapy import Socrata

client = Socrata("healthdata.gov", None)
now = datetime.datetime.now()

def main():
	part_one()
	part_two()
	part_three()

def part_one():
	df = read_data()
	total_tests = get_total_tests_for_yesterday(df)

	print('Total tests as of yesterday:', total_tests)

AVG_LENGTH = 7
NUMBER_OF_DAYS = 30
def part_two():
	df = read_data()

	rolling_average_with_date = get_rolling_averages(df, AVG_LENGTH, NUMBER_OF_DAYS)
	
	plt.plot(*zip(*rolling_average_with_date))
	plt.gca().xaxis.set_major_locator(plt.MultipleLocator(6))
	plt.title('Total rolling 7 day average over past 30 days')
	plt.xlabel('Date')
	plt.ylabel('Rolling average (number of cases)')
	plt.savefig(f'figures/rolling_average.png') 
	print('Rolling average for the past 30 days (see figures/rolling_average.png for visualization):', rolling_average_with_date)

NUMBER_OF_STATES = 10
def part_three():
	df = read_data()

	oldest_date = now - datetime.timedelta(days=NUMBER_OF_DAYS) # TODO: Different variable?
	datestr = f'{oldest_date.year}-{oldest_date.month}-{oldest_date.day}' 

	df = df[df.date > datestr]

	unique_states = df.state.unique()
	positivity_rate_with_state = []

	for state in unique_states:
		state_data = df[df.state == state]
		total_tests = state_data['new_results_reported'].sum()
		positive = state_data[state_data.overall_outcome == 'Positive']['new_results_reported'].sum()

		positivity_rate_with_state.append((state, round(positive / total_tests, 2)))
	
	positivity_rate_with_state.sort(key=lambda a: a[1], reverse=True)
	print('Top ten positivity rates:', positivity_rate_with_state[:NUMBER_OF_STATES])

def read_data():
	df = pd.read_csv('data/Dataset.csv', dtype={
	    'state': 'string',
	    'state_name': 'string',
	    'state_fips': 'int64',
	    'fema_region': 'string',
	    'overall_outcome': 'string',
	    'new_results_reported': 'int64',
	    'total_results_reported': 'int64',
	    'geocoded_state': 'float64',
	})

	df['date'] = pd.to_datetime(df['date'])

	return df

main()
