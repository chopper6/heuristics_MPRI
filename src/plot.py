from matplotlib import pyplot as plt
from util import *
import numpy as np, os
from datetime import datetime, date

COLORS = ['blue','red','green','purple','cyan','orange','brown','magenta','yellow','grey']
#COLORS = ['#66ff33','#cc66ff','#ff0066','#00ffff','#006699','#6600cc','#cc0066','#ff6666']




def solvers_x_features(feats, params, global_param_title):
	# features should be a dict of different features
	# features[feature] is a dict of solvers
	# features[feature][solver] is a dict with 'avg', 'var'
	# features[feature][solver]['avg'] = [array with one value for each iteration]
	
	# params should be 'global' ones
	assert(os.path.isdir(params['out_dir']))

	now = datetime.now()
	curr_date = str(date.today()).strip('2020-')
	curr_time = str(datetime.now().strftime("%H-%M-%S"))
	tstamp = curr_date+'_'+curr_time

	for feat_name in feats.keys():
		plot_a_feature(feats, feat_name, params, global_param_title, tstamp)



def plot_a_feature(feats, feat_name, params, global_param_title, tstamp):
	iters = params['iters']
	plt.figure(1,[12,8])
	time = [i for i in range(iters+1)]
	handles = []
	feat = feats[feat_name]
	i=0
	for k in feat.keys():
		c = COLORS[i%len(COLORS)]
		plt.plot(time,feat[k]['avg'],alpha=1, linewidth=1, color=c)
		plt.errorbar(time,feat[k]['avg'],yerr=feat[k]['var'],alpha=.1, color=c)
		handles += [k]
		i+=1
	plt.legend(handles)
	plt.xlabel('Time')
	plt.ylim(-.1,1.1)
	plt.ylabel(feat_name)

	if params['write_params']:
		ax = plt.gca()
		ax.text(0,-.2,'PARAMS' + global_param_title[:120])
		ax.text(0,-.25,global_param_title[120:240])

	plt.savefig(params['out_dir']+tstamp+'_'+feat_name+'.png')
	plt.clf()
	plt.close()
