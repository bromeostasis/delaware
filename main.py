import pandas as pd
import datetime
from sodapy import Socrata


client = Socrata("healthdata.gov", None)

def main():
	part_two()

def part_one():
	df = pd.read_csv('data/Dataset.csv')
	df = df.sort_values(by='total_results_reported', ascending=False)

	unique_states = df.state.unique()
	unique_outcomes = df.overall_outcome.unique()

	total_tests = 0

	for state in unique_states:
		state_results = df[df.state == state]
		for outcome in unique_outcomes:
			# print(state, outcome)
			state_outcome_results = state_results[state_results.overall_outcome == outcome]
			# print(len(outcome))
			if len(state_outcome_results) > 0:
				total_tests += state_outcome_results.iloc[0]['total_results_reported']
				# print(state_outcome_results.iloc[0]['total_results_reported'])
				# print(df.query(f'state == "{state}" & overall_outcome == "{outcome}"').iloc[0]['total_results_reported'])

	print('total tests as of yesterday', total_tests)

AVG_LENGTH = 7
NUMBER_OF_DAYS = 30
def part_two():
	# We start calculating on the seventh day, so subtract one
	dataset_length = NUMBER_OF_DAYS - 1 + AVG_LENGTH
	now = datetime.datetime.now()
	oldest_date = now - datetime.timedelta(days=dataset_length)

	datestr = f'{oldest_date.year}-{oldest_date.month}-{oldest_date.day}' 

	results = client.get("j8mb-icvb", where=f'date >= "{datestr}"', limit=10000)

	df = pd.DataFrame.from_records(results)

	df['date'] = pd.to_datetime(df['date'])
	df['new_results_reported'] = pd.to_numeric(df['new_results_reported'])

	# print(df.head())

	rolling_average_with_date = []
	total_new_case_queue = []
	for i in range(dataset_length):
		# print(i)
		# print(oldest_date + datetime.timedelta(days=i))
		current_date = oldest_date + datetime.timedelta(days=i)
		datestr = f'{current_date.year}-{current_date.month}-{current_date.day}'
		new_tests_on_current_date = df.query(f'date == "{datestr}"')['new_results_reported'].sum()
		total_new_case_queue.append(new_tests_on_current_date)
		if len(total_new_case_queue) == AVG_LENGTH:
			rolling_average_with_date.append((datestr, round(sum(total_new_case_queue) / AVG_LENGTH, 2)))
			total_new_case_queue.pop(0)

	print('Rolling average for the past 30 days', rolling_average_with_date)

main()
