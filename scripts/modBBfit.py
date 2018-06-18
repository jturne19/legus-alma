"""
"""
from scipy.optimize import curve_fit
import numpy as np
from astropy import constants as const
import emcee


def fit(freqH, fluxH, errH, sr_in_images):
	"""
	fits a modified blackbody to the herschel (H) fluxes
	
	based on:
	http://dan.iel.fm/emcee/current/user/line/
	~turner/Documents/ASTR5160/turner/week14/emcee_sample.py


	freqH:			frequencies of the herschel PACS and SPIRE data
	fluxH:			flux (in Jy) of the herschel data
	errH:			errors for the herschel data
	sr_in_images:	the total sr in the PACS/SPIRE images

	Outputs:
	beta_mcmc:		[best fit beta value, +error, -error]
	T_mcmc:			[best fit temp value, +error, -error]
	"""

	# define some constants that help simplify the BB equations
	# 2 * h * c^2 
	C1 = 2 * const.h.value * const.c.value**2 
	# define constant for the planck function exponent
	C2 = const.h.value * const.c.value / const.k_B.value
	
	C3 = 2 * const.h.value / const.c.value**2
	C4 = const.h.value / const.k_B.value


	def lnlike(theta, freq, flux, flux_err):
		""" function for the natural log of the likelihood function. assumes a gaussian error.
		
		Inputs:
		theta: needed for the mcmc optimizing stuff. holds our beta and T guesses
		lam: wavelengths in meters
		flux: flux in 
		flux_err: the error in the flux measurments
		
		"""
		beta, T = theta
		return -0.5*(np.sum((flux-mbb_func_freq(freq, beta, T))**2/(flux_err**2) - np.log(2*np.pi*flux_err**2)))
	
	def lnprior(theta):
		""" define the prior function since we know beta cannot be less than 0 and probably won't be more than 10
		T won't be less than 3 K and probably won't be more than 100 K (maybe? something to ask danny about)
	
		"""
		beta, T = theta
		if 1 < beta < 4 and 3 < T < 100:
			return 0.0
		return -np.inf
	
	def lnprob(theta, freq, flux, flux_err):
		""" full log probability function (posterior probability)
	
		"""
		lp = lnprior(theta)
		if not np.isfinite(lp):
			return -np.inf
		return lp + lnlike(theta, freq, flux, flux_err)
	

	def mbb_func_lam(lam, beta, T):
		bb = C1 * (lam**(beta - 5.0)) / (np.exp(C2/(lam*T)) - 1)
		return bb * lam * sr_in_images
	
	def mbb_func_freq(freq, beta, T):
		bb = C3 * (freq**(3 + beta)) / (np.exp(C4*freq/T) - 1)
		return bb * freq * sr_in_images
	

	# make an initial guess for beta and T
	initial_guess = np.array([2, 20])
	
	# initialize walkers in a tiny gaussian ball around the initial guesses
	ndim, nwalkers = 2, 1000
	pos = [initial_guess + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]
	
	# set up the sampler
	sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(freqH, fluxH, errH))
	# run the MCMC sampler for 500 steps starting at the gaussian ball
	sampler.run_mcmc(pos, 500)
	# discard the first 50 steps and flatten the chain array
	samples = sampler.chain[:, 50:, :].reshape((-1, ndim))

	beta_mcmc, T_mcmc = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), zip(*np.percentile(samples, [16,50,84], axis=0)))

	return beta_mcmc, T_mcmc
