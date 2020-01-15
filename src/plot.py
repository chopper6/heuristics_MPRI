from matplotlib import pyplot as plt
from util import *
import numpy as np, os
from datetime import datetime, date

COLORS = ['blue','red','green','purple','orange','brown']
#COLORS = ['#66ff33','#cc66ff','#ff0066','#00ffff','#006699','#6600cc','#cc0066','#ff6666']




def solvers_x_features(feats, params):
	# features should be a dict of different features
	# features[feature] is a dict of solvers
	# features[feature][solver] is a dict with 'avg', 'var'
	# features[feature][solver]['avg'] = [array with one value for each iteration]
	
	# params should be 'global' ones
	assert(os.path.isdir(params['out_dir']))

	for feat_name in feats.keys():
		plot_a_feature(feats, feat_name, params)



def plot_a_feature(feats, feat_name, params):
	iters = params['iters']
	plt.figure(1,[4,3])
	time = [i for i in range(iters+1)]
	handles = []
	feat = feats[feat_name]
	i=0
	for k in feat.keys():
		c = COLORS[i%len(COLORS)]
		plt.plot(time,feat[k]['avg'],alpha=1, linewidth=1, color=c)
		plt.errorbar(time,feat[k]['avg'],yerr=feat[k]['var'],alpha=.3, color=c)
		handles += [k]
		i+=1
	plt.legend(handles)
	plt.xlabel('Time')
	plt.ylabel(feat_name)
	now = datetime.now()
	curr_date = str(date.today()).strip('2020-')
	curr_time = str(datetime.now().strftime("%H-%M-%S"))
	plt.savefig(params['out_dir']+curr_date+'_'+curr_time+'_'+feat_name+'.png')
	plt.clf()
	plt.close()
