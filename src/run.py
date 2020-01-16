import features, evolve
import numpy as np, random as rd

def one_instance(params,feat, rep):

	P = evolve.init(params)
	evolve.eval(P,params) #assigns fitness
	feats = features.append(P, feat, params,0,rep) #init msmt, alt could first do one round of selection

	for i in range(params['iters']):

		evolve.select(P,params) #sets P['survive'][i] = 1|0 for each indiv in population
		evolve.breed(P,params) #replace 'dead' indivs, includes crossover
		evolve.mutate(P,params) #flipin' bits
		evolve.eval(P,params) #assigns fitness

		feats = features.append(P, feat, params,i+1,rep) #msre AFTER update
		if params['debug']: evolve.check(P,params)
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

