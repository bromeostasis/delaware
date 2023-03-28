import datetime

def get_total_tests_for_yesterday(df):
	df = df.sort_values(by='total_results_reported', ascending=False)

	unique_states = df.state.unique()
	unique_outcomes = df.overall_outcome.unique()

	total_tests = 0

	for state in unique_states:
		state_results = df[df.state == state]
		for outcome in unique_outcomes:
			state_outcome_results = state_results[state_results.overall_outcome == outcome]
			if len(state_outcome_results) > 0:
				total_tests += state_outcome_results.iloc[0]['total_results_reported']

	return total_tests

def get_rolling_averages(df, average_length, number_of_days):
	# We start calculating on the seventh day, so subtract one
	dataset_length = number_of_days - 1 + average_length
	
	now = datetime.datetime.now()
	oldest_date = now - datetime.timedelta(days=dataset_length)
	datestr = f'{oldest_date.year}-{oldest_date.month}-{oldest_date.day}' 

	df = df[df.date >= datestr]

	rolling_average_with_date = []
	total_new_case_queue = []
	for i in range(dataset_length):
		current_date = oldest_date + datetime.timedelta(days=i)
		datestr = f'{current_date.year}-{current_date.month}-{current_date.day}'
		new_cases_on_current_date = df.query(f'date == "{datestr}" & overall_outcome == "Positive"')['new_results_reported'].sum()
		total_new_case_queue.append(new_cases_on_current_date)
		if len(total_new_case_queue) == average_length:
			rolling_average_with_date.append((datestr, round(sum(total_new_case_queue) / average_length, 2)))
			total_new_case_queue.pop(0)

	return rolling_average_with_date

def get_top_states_by_positivity_rate(df, number_of_days, number_of_states):
	now = datetime.datetime.now()
	oldest_date = now - datetime.timedelta(days=number_of_days)
	datestr = f'{oldest_date.year}-{oldest_date.month}-{oldest_date.day}' 

	df = df[df.date >= datestr]

	unique_states = df.state.unique()
	positivity_rate_with_state = []

	for state in unique_states:
		state_data = df[df.state == state]
		total_tests = state_data['new_results_reported'].sum()
		positive = state_data[state_data.overall_outcome == 'Positive']['new_results_reported'].sum()

		positivity_rate_with_state.append((state, round(positive / total_tests, 2)))
	
	positivity_rate_with_state.sort(key=lambda a: a[1], reverse=True)
	return positivity_rate_with_state[:number_of_states]

