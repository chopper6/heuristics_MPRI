import features 
import numpy as np, random as rd

def one_instance(params,feat, rep):
	n =params['pop_size']
	P = {} #POPULATION, normally would add P['query'] or whatever too
	# need to track the individuals seperately to allow for effic numpy
	P['fitness'] = np.array([1 for i in range(n)])

	feats = features.append(P, feat, params,0,rep) #init msmt
	for i in range(params['iters']):

		# MAIN EVOLUTIONARY ALGORITHM GOES HERE

		# was just using the line below for debug
		P['fitness'] = np.multiply([rd.random()*rd.choice([-2,2]) for i in range(n)],P['fitness'])
		
		feats = features.append(P, feat, params,i+1,rep) #msre AFTER update
	return feats

#########################################################################################

def batch(batch_params):
	all_features = features.init_all()
	for param_title in batch_params.keys(): #extract beforehand
		if param_title != 'global':
			params = batch_params[param_title]

			# avg,var over many reps
			param_features = features.init_a_set(params)
			for r in range(params['repetitions']):
				one_instance(params, param_features,r) #appends to feature set internally
			all_features = features.merge_to_all(param_features, all_features, param_title) 

	return all_features

