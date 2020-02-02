from util import *
import numpy as np

# different metrics of an EA population at different iterations

# ADD NEW FEATURES BY ADDING TO THE LIST 'FEATURE NAMES', AND ADDING A LINE IN 'APPEND()'

FEATURE_NAMES = ['avg_fitness','max_fitness','pre_var_fitness','time x pop','mutation_rate','surving_pop_size','cumulative error']  #'var_fitness','pre_avg_fitness'

def append(population,features, params,iteration,rep):
	features['avg_fitness'][iteration][rep] = np.average(population['fitness'])
	features['max_fitness'][iteration][rep] = np.max(population['fitness']) 
	
	# characteristics of popn before selection, i.e. what variation is being generated
	features['pre_var_fitness'][iteration][rep] = np.var(population['pre_selection_fitness']) 

	features['mutation_rate'][iteration][rep] = params['mutation_rate']
	features['surving_pop_size'][iteration][rep] = params['parent_size']


	# currently assumes plus selection
	if iteration == 0:
		features['time x pop'][iteration][rep] = params['child_size']
		features['cumulative error'][iteration][rep] = 1-max(population['fitness'])/(params['length'])

	else:
		features['time x pop'][iteration][rep] = params['child_size']+features['time x pop'][iteration-1][rep]

		features['cumulative error'][iteration][rep] = 1-max(population['fitness'])/(params['length'])
		features['cumulative error'][iteration][rep] += features['cumulative error'][iteration-1][rep]

	if params['selection'] == 'comma':
		features['time x pop'][iteration][rep] += params['parent_size']

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

		if k not in ['surving_pop_size','mutation_rate','cumulative error']:
			normz = params['length']
		else:
			normz = 1
		calcd_feat[k]['avg'] = [np.average(param_feat[k][i])/normz for i in rng(param_feat[k])]
		calcd_feat[k]['var'] = [np.var(param_feat[k][i])/normz for i in rng(param_feat[k])]
		all_feat[k][title] = calcd_feat[k]
	return all_feat

