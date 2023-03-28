import matplotlib.pyplot as plt

def plot_rolling_averages_over_time(rolling_average_with_date):
	plt.plot(*zip(*rolling_average_with_date))
	plt.gca().xaxis.set_major_locator(plt.MultipleLocator(6))
	plt.title('Rolling 7 day average of positive cases over past 30 days')
	plt.xlabel('Date')
	plt.ylabel('Rolling average (number of positive cases)')
	plt.savefig(f'figures/rolling_average.png') 