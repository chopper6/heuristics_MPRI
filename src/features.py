from util import *
import numpy as np

# different metrics of an EA population at different iterations

# ADD NEW FEATURES BY ADDING TO THE LIST 'FEATURE NAMES', AND ADDING A LINE IN 'APPEND()'

FEATURE_NAMES = ['avg_fitness','var_fitness','max_fitness'] #add more

def append(population,features, params,iteration,rep):
	features['avg_fitness'][iteration][rep] = np.average(population['fitness']) #/params['length']
	features['var_fitness'][iteration][rep] = np.var(population['fitness']) #/params['length']
	features['max_fitness'][iteration][rep] = np.max(population['fitness']) #/params['length']
	# features is the dataset so far
	return features



#########################################################################################

def init_a_set(params):
	# features should be a dict of different features
	# features[feature] is a dict of solvers
	# features[feature][param_title] is a dict with 'avg', 'var'
	# features[feature][param_title]['avg'] = [array with one value for each iteration]

	feat = {}
	for name in FEATURE_NAMES:
		feat[name]=[np.empty(params['repetitions']) for i in range(params['iters']+1)]
	return feat



def init_all():
	feat = {}
	for name in FEATURE_NAMES:
		feat[name]={} #dict for each param_set
	return feat

def merge_to_all(param_feat, all_feat, title,params):
	# title is for the param_set
	calcd_feat = {}
	for k in param_feat.keys():
		calcd_feat[k] = {}
		calcd_feat[k]['avg'] = [np.average(param_feat[k][i])/params['length'] for i in rng(param_feat[k])]
		calcd_feat[k]['var'] = [np.var(param_feat[k][i])/params['length'] for i in rng(param_feat[k])]
		all_feat[k][title] = calcd_feat[k]
	return all_feat

