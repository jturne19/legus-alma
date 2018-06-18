"""
"""
import numpy as np

def mcmc_error(function, x, y, sigma):
	""" 
	use mcmc to generate errors bars for a fitting function

	Inputs:
	func:	:function:	the mathematical function for which you are fitting your data points
	x:		:array:		array of x values of data points
	y1:		:array:		array of y values of data points
	sigma:	:array:		array of sigma (uncertainties/errors) for the data points 

	"""
	# get number of data points in data set
	num_data_points = len(x)


	# number of iterations to run through
	num_iters = 100000
	# generate gaussian distributed random numbers about the 
	r = np.zeros([num_iters, num_data_points])
	for i in range(len(x)):
		r[:,i] = np.random.normal(y[i], sigma[i], num_iters)


	values = np.zeros(num_iters+1)

	for i in range(len(values)):
		if i == 0:
			v = function(x,y)
			values[i] = v
		else:
			v = function(x, r[i-1])
			values[i] = v 

	mean = np.mean(values)
	std = np.std(values)
	median = np.median(values)

	return mean, std, median


if __name__ == '__main__':
	None