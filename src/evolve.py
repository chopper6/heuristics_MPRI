import numpy as np, random as rd
from util import *

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
	P['pre_selection_fitness'] = np.zeros(n) #just for a measurement
	P['parents'] = np.random.choice([i for i in range(c)], size=(n,m))
	P['children'] = np.random.choice([i for i in range(c)], size=(l,m))
	P['solution'] = np.random.choice([i for i in range(c)], size=(m,))
	return P

def check(P, params):
	# just for debugging purposes
	n,l,m,c = params['pop_size'], params['child_size'], params['length'], params['colors']
	assert(len(P['fitness'])==n)	
	assert(len(P['survive'])==n)	
	assert(np.shape(P['parents'])==(n,m))
	assert(np.shape(P['children'])==(l,m))
	assert(len(P['solution']) == m)


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
	P['pre_selection_fitness'] = [eval_string(t[i],P,params) for i in rng(t)]
	indx = np.argpartition(ev, -params['pop_size'])[-params['pop_size']:]
	P['parents'] = t[indx]
	P['fitness'] = ev[indx]
		 

def distribution_of_majority(P, params):
	p = P['parents']
	res = [None] * params['length']
	for i in range(params['length']):
		res[i] = np.zeros(params['colors'])
		unique, counts = np.unique(p[:,i], return_counts=True)
		for t in zip(unique, counts):
			res[i][t[0]] = t[1]/float(params['pop_size'])
	return res

def correct_flip_vector(M, parent, params):
	res = np.zeros(len(parent))

	for i in range(params['length']):
		if M[i]:
			c = parent[i]
			res[i] = rd.choice([x for x in range(params['colors']) if x != c])
			
	return res

def variation(P, params):
	variation_mode = params['variation']
	crossover_mode = params['crossover']
	mutation_mode = params['mutation']
	n, l, m, c, v = params['pop_size'], params['child_size'], params['length'], params['colors'], params['crossover_rate']

	if variation_mode == 'mutex': # if not crossover, then mutation 
		for i in range(l):
			if rd.random() < v: # crossover part
				if crossover_mode == 'rand':	
					parents = rd.choices(P['parents'], k=2) #py 3.8 req'd, else use the line below
					#parents = [rd.choice(P['parents']) for i in range(2)]
					which_parent = np.random.choice([0,1],size=m)
					child = np.multiply(which_parent,parents[0])+np.multiply(1-which_parent,parents[1]) 

				elif crossover_mode == 'n-rand':	
					parents = rd.choices(P['parents'], k=m) #py 3.8 req'd, else use the line below
					#parents = [rd.choice(P['parents']) for i in range(m)]
					child = [parents[i][i] for i in range(m)]

				elif crossover_mode == 'majority':
					distr = distribution_of_majority(P,params)
					child = np.array([ np.random.choice(c, 1, p=distr[pos]) for pos in range(m)]) 
					
				elif crossover_mode == 'random_restart':
					child = np.random.choice([j for j in range(c)],size=m)

				else: assert(False)

			else:	# mutation part
				if mutation_mode == 'simple':
					M = np.random.binomial(1, params['mutation_rate'], (m,))
					C = np.random.randint(c, size=(m,))
					child = np.multiply(M,C) + np.multiply(1-M, rd.choice(P['parents']))
				elif mutation_mode == 'simple_new':
					M = np.random.binomial(1, params['mutation_rate'], (m,))
					parent = rd.choice(P['parents'])
					child = np.multiply(M,correct_flip_vector(M, parent, params)) + np.multiply(1-M, parent)
				elif mutation_mode == 'flip':
					indx = rd.sample(range(params['length']), params['k'])
					M = np.zeros(m)
					M[indx] = 1
					parent = rd.choice(P['parents'])
					child = np.multiply(M,correct_flip_vector(M, parent, params)) + np.multiply(1-M, parent)
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