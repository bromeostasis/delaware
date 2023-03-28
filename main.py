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
	top_ten_states = get_top_states_by_positivity_rate(df, NUMBER_OF_DAYS, NUMBER_OF_STATES)
	print('Top ten positivity rates:', top_ten_states)


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
