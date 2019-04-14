import numpy as np

def compute_gradient(density_matrix, projectors, term_frequencies):
	gradient = np.zeros(density_matrix.shape)
	for i in range(len(projectors)):
		projector = projectors[i]
		tf = term_frequencies[i]
		delta = tf / np.trace(np.dot(projector, density_matrix)) * projector
		gradient += delta
	return gradient

def compute_q(trace_gdg, t):
	return 1 + 2 * t + t ** 2 * trace_gdg

def compute_direction_bar(density_matrix, gradient):
	return (np.dot(gradient, density_matrix) + np.dot(density_matrix, gradient)) / 2 - density_matrix

def compute_direction_tild(density_matrix, gdg, trace_gdg):
	return gdg / trace_gdg - density_matrix

def compute_direction(density_matrix, projectors, term_frequencies, t):
	gradient = compute_gradient(density_matrix, projectors, term_frequencies)
	gdg = np.dot(np.dot(gradient, density_matrix), gradient)
	trace_gdg = np.trace(gdg)
	
	d_bar = compute_direction_bar(density_matrix, gradient)
	d_tild = compute_direction_tild(density_matrix, gdg, trace_gdg)
	
	q_t = compute_q(trace_gdg, t)
		
	return 2 / q_t * d_bar + t * trace_gdg / q_t * d_tild

def compute_objective():
	pass

def gqlm(projectors, term_frequencies, t = 0.5):
	epsilon = 1e-5
	num_epoch = 200
	
	num_words = len(term_frequencies)
	
	diagonal_entries = np.random.rand(num_words)
	
	diagonal_entries /= np.sum(diagonal_entries)
	density_matrix = np.diag(diagonal_entries)
		
	i = 0	
	stop_criterion = False	
	while not stop_criterion:	
		delta = t * compute_direction(density_matrix, projectors, term_frequencies, t)
		density_matrix += delta
		
		stop_criterion = i > num_epoch
		i +=1 
		
	return density_matrix
	
