import numpy as np, random as rd

# TODO: debug breed, esp crossover = 'uniform2', fix eval (curr the all one string)
# TODO: maybe a bug...? With 0 mutation monotonic increase of max fitness, but even .01 mutation is very noise ...

# in general n=pop_size, m=problem_string_lng, c=num_colors

def init(params):
	# assume init all values to purely random
	n,m,c = params['pop_size'], params['length'], params['colors']
	P = {}
	P['fitness'] = np.array([0 for i in range(n)])
	P['survive'] = np.array([1 for i in range(n)])
	P['values'] = np.random.choice([i for i in range(c)],size=(n,m))
	return P

def check(P, params):
	# just for debugging purposes
	# add more
	n,m,c = params['pop_size'], params['length'], params['colors']
	assert(len(P['fitness'])==n)	
	assert(len(P['survive'])==n)	
	assert(np.shape(P['values'])==(n,m))

def mutate(P,params):
	# worried that this won't retain INT's
	n,m,c = params['pop_size'], params['length'], params['colors']
	M, C = np.random.rand(n,m), np.random.choice([i for i in range(c)],size=(n,m))

	# better np way
	for i in range(n):
		for j in range(m):
			if M[i][j] < params['mutation_rate']: M[i][j] =1
			else: M[i][j]=0

	P['values'] = np.multiply(M,C) + np.multiply(1-M,P['values'])

def select(P,params):
	sorted_indices = np.flip( np.argsort(P['fitness'],axis=0) )

	# faster np method?
	for i in range(params['pop_size']):
		if i in sorted_indices[:params['num_survive']]: 
			P['survive'][i] = 1
		else: 
			P['survive'][i] = 0

def breed(P, params):

	xover, n, m, c = params['crossover'], params['pop_size'], params['length'], params['colors']
	# faster np method?
	for i in range(params['pop_size']):
		if P['survive'][i] == 0:
			# ughly
			# eventually might want to rewrite diff crossovers as functions
			if xover == 'asex':

				# i know theres a np fn for this, but can't find it:
				surv_indices = []
				for i in range(n):
					if P['survive'][i] == 1: surv_indices += [i]

				parent = rd.choice(surv_indices)
				child = np.copy(P['values'][parent])
			elif xover in ['rand','random']:
				child = np.random.choice([j for j in range(c)],size=m)
			elif xover == 'uniform2':
				parent1 = parent2 = rd.random.choice([np.argwhere(P['survive'])])
				while parent1 == parent2:
					parent2 = rd.random.choice([np.argwhere(P['survive'])])
				which_parent = np.random.choice([0,1],size=m)
				p1, p2 = np.copy(P['values'][parent1]), np.copy(P['values'][parent2]) # maybe not nec, i'm not sure
				child = np.multiply(which_parent,p1)+np.multiply(1-which_parent,p2) 
			else: assert(False) #unknown crossover param

			P['values'][i] = child 

def eval(P, params):
	# TEMP: JUST USING ALL ONE STRING AS TARGET

	n,m,c = params['pop_size'], params['length'], params['colors']
	P['fitness'] = np.sum(np.multiply(np.ones((n,m)),P['values']),axis=1)