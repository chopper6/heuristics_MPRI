import features, evolve
import numpy as np, random as rd

def one_instance(params,feat, rep):
	P = evolve.init(params)
	# assign fitness for the first generation (not necessary though!)
	ev = list(map(lambda s: evolve.eval_string(s, P, params), P['parents']))
	P['fitness'] = ev 

	feats = features.append(P, feat, params,0,rep) #init msmt, alt could first do one round of selection

	for i in range(params['iters']):

		evolve.variation(P,params)
		evolve.select(P,params)

		feats = features.append(P, feat, params,i+1,rep) #msre AFTER update
		if params['debug']: 
			evolve.check(P,params)
	return feats

#########################################################################################

def batch(batch_params):
	all_features = features.init_all()
	for param_title in batch_params.keys(): #extract beforehand
		if param_title != 'global':
			print("Running evolution with",param_title)
			params = batch_params[param_title]

			# avg,var over many reps
			param_features = features.init_a_set(params)
			for r in range(params['repetitions']):
				one_instance(params, param_features,r) #appends to feature set internally
			all_features = features.merge_to_all(param_features, all_features, param_title, params) 

	return all_features

