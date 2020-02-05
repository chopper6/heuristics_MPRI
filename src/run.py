import features, evolve
import numpy as np, random as rd, time

def one_instance(params,feat, rep):
	P = evolve.init(params)
	
	# assign fitness for the first generation (not necessary though!)
	ev = list(map(lambda s: evolve.eval_string(s, P, params), P['parents']))
	P['fitness'] = ev 

	feats = features.append(P, feat, params,0,rep) #init msmt, alt could first do one round of selection

	init_params = params.copy() #for dynamic params
	rep_params = params.copy() #dynamics will overwrite as it goes

	var_t, sel_t,feat_t,che_t = 0,0,0,0

	for i in range(params['iters']):

		#t0=time.time()
		evolve.variation(P,rep_params, i, init_params)
		#t1=time.time()
		evolve.select(P,rep_params)
		#t2=time.time()

		feats = features.append(P, feat, rep_params,i+1,rep) #msre AFTER update
		#t3=time.time()
		if params['debug']: 
			evolve.check(P,rep_params)
		#t4=time.time()

		#var_t += t1-t0
		#sel_t += t2-t1
		#feat_t += t3-t2
		#che_t += t4-t3

	#times = {'var':var_t,'sel':sel_t,}
	#print(var_t,sel_t,feat_t,che_t)

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

