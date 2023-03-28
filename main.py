import pandas as pd

def main():
	part_one()

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


main()
