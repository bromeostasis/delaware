import pandas as pd

from calculations.calculations import *
from plotting.plotting import *
from tabulate import tabulate

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

	plot_rolling_averages_over_time(rolling_average_with_date)

	rolling_average_with_date.insert(0, ('Date', 'Rolling Average'))
	print('Rolling average for the past 30 days (see figures/rolling_average.png for visualization):')
	print(tabulate(rolling_average_with_date, headers='firstrow', tablefmt='fancy_grid', floatfmt='.2f'))

NUMBER_OF_STATES = 10
def part_three():
	df = read_data()
	top_ten_states = get_top_states_by_positivity_rate(df, NUMBER_OF_DAYS, NUMBER_OF_STATES)
	print('Top ten positivity rates:')
	top_ten_states.insert(0, ('State', 'Positivity Rate'))
	print(tabulate(top_ten_states, headers='firstrow', tablefmt='fancy_grid', floatfmt='.2f'))


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
