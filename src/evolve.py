import numpy as np, random as rd

# TODO: debug breed, debug eval, esp crossover = 'uniform2', fix eval (curr the all one string)
# TODO: maybe a bug...? With 0 mutation monotonic increase of max fitness, but even .01 mutation is very noise ...
# TEMP: JUST USING ALL ONE STRING AS TARGET
# add: mutation only kept if improves

# in general n=pop_size, m=problem_string_lng, c=num_colors

def init(params):
	# assume init all values to purely random
	n,l,m,c = params['pop_size'], params['child_size'], params['length'], params['colors']
	P = {}
	P['fitness'] = np.zeros(n)
	P['survive'] = np.ones(n)
	P['values'] = np.random.choice([i for i in range(c)], size=(n,m))
	P['parents'] = np.random.choice([i for i in range(c)], size=(n,m))
	P['children'] = np.random.choice([i for i in range(c)], size=(l,m))
	P['solution'] = np.random.choice([i for i in range(c)], size=(m,))
	return P

def check(P, params):
	# just for debugging purposes
	# add more
	n,l,m,c = params['pop_size'], params['child_size'], params['length'], params['colors']
	assert(len(P['fitness'])==n)	
	assert(len(P['survive'])==n)	
	assert(np.shape(P['parents'])==(n,m))
	assert(np.shape(P['children'])==(l,m))
	assert(len(P['solution']) == m)

def mutate(P,params):
	# POSS MUTATION: flip k
	mode = params['mutation']

	n,m,c = params['pop_size'], params['length'], params['colors']
	M = np.random.binomial(1, params['mutation_rate'], (n,m))
	C = np.random.randint(c, size=(n,m))
	if mode == 'simple':
		P['values'] = np.multiply(M,C) + np.multiply(1-M,P['values'])
	else: assert(False)

def eval_string(s, P, params):
	return np.sum(P['solution']  == s)

def select(P,params):
	mode = params['selection']
	# POSS SELECTION: simulated annealing

	if (mode == 'plus'):
		t = np.vstack((P['parents'],P['children']))
	elif (mode == 'comma'):
		t = P['children']
	else: assert(False)
	
	ev = np.array(list(map(lambda s: eval_string(s, P, params), t)))
	indx = np.argpartition(ev, -params['pop_size'])[-params['pop_size']:]
	P['parents'] = t[indx]
	P['fitness'] = ev[indx]
		
def breed(P, params):
	# POSS CROSSOVER: weighted crossover by fitness, majority vote
	# similar behav with diff number of parents, just diff if pick by fitness-weighted

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

def variation(P, params):
	variation_mode = params['variation']
	crossover_mode = params['crossover']
	mutation_mode = params['mutation']
	n, l, m, c, v = params['pop_size'], params['child_size'], params['length'], params['colors'], params['variation_rate']

	if variation_mode == 'mutex': # if not crossover, then mutation 
		for i in range(l):
			if rd.random() > v: # crossover part
				parents = rd.choices(P['parents'], k=2)
				which_parent = np.random.choice([0,1],size=m)
				child = np.multiply(which_parent,parents[0])+np.multiply(1-which_parent,parents[1]) 
			else:	# mutation part
				M = np.random.binomial(1, params['mutation_rate'], (m,))
				C = np.random.randint(c, size=(m,))
				child = np.multiply(M,C) + np.multiply(1-M, rd.choice(P['parents']))
			P['children'][i] = child
	elif variation_mode == 'sbm_only':
		for i in range(l):
			M = np.random.binomial(1, params['mutation_rate'], (m,))
			C = np.random.randint(c, size=(m,))
			P['children'][i] = np.multiply(M,C) + np.multiply(1-M, rd.choice(P['parents']))

#def eval(P, params):

#	l,m,c = params['child_size'], params['length'], params['colors']
#	for i in range(l):
#		P['fitness_children'][i] = np.sum(P['solution']  == P['children'][i])