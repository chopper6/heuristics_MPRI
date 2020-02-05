from matplotlib import pyplot as plt
from util import *
import numpy as np, os, pickle
from datetime import datetime, date

COLORS = ['blue','red','green','purple','cyan','orange','brown','magenta','yellow','grey']
#COLORS = ['#66ff33','#cc66ff','#ff0066','#00ffff','#006699','#6600cc','#cc0066','#ff6666']




def solvers_x_features(feats, params, global_param_title):
	
	if not os.path.isdir(params['out_dir']):
		os.mkdir(params['out_dir'])


	now = datetime.now()
	curr_date = str(date.today()).strip('2020-')
	curr_time = str(datetime.now().strftime("%H-%M-%S"))
	tstamp = curr_date+'_'+curr_time



	with open(params['out_dir'] + tstamp + '_dump.pickle','wb') as file:
		data = {'feats':feats, 'params':params}
		pickle.dump(str(data), file) 

	if params['write_params_txt']:
		with open(params['out_dir']+tstamp+'_params.txt','w') as f:
			f.write(str(params))


	for feat_name in feats.keys():
		if feat_name != 'time x pop':
			plot_a_feature(feats, feat_name, params, global_param_title, tstamp)

		if params['time_x_pop_plots']:
			plot_a_feature(feats, feat_name, params, global_param_title, tstamp,variable_time=True)



def plot_a_feature(feats, feat_name, params, global_param_title, tstamp, variable_time=False):

	plt.figure(1,[16,12])


	if variable_time: 
		time = feats['time x pop']

	elif 'iters' not in params.keys(): #ie iters is a batch param itself
		None # sloppy, will initialize below

	else:
		iters = params['iters']
		time = [i for i in range(iters+1)]

	handles = []
	feat = feats[feat_name]
	i=0
	for k in feat.keys():
		c = COLORS[i%len(COLORS)]

		if variable_time: 
			this_time = time[k]['avg']

		elif 'iters' not in params.keys(): #ie iters is a batch param itself
			this_time = [i for i in rng(feat[k]['avg'])]

		else:
			this_time = time

		plt.semilogx(this_time,feat[k]['avg'],alpha=1, linewidth=3, color=c)

		# just for final plots
		if params['colors'] == 2: lw = 4
		else: lw = 2
		b, d = np.array(feat[k]['avg']) + np.array(feat[k]['var']), np.array(feat[k]['avg']) - np.array(feat[k]['var'])
		
		plt.fill_between(np.array(this_time),b,d,alpha=.2, color=c)

		handles += [k]
		i+=1
	plt.legend(handles, fontsize=28)
	plt.xlabel('Time',fontsize=28)
	plt.xticks(fontsize=24)
	
	if feat_name not in ['entropy','surving_pop_size','mutation_rate','cumulative error','variance in fitness']:
		plt.axhline(y=1, color='grey', linestyle='--', alpha=.5)
		plt.ylim(-.1,1.1)

	plt.ylabel(feat_name,fontsize=28)
	plt.yticks(fontsize=24)
	if params['write_params_on_img']:
		ax = plt.gca()
		ax.text(0,-.2,'PARAMS' + global_param_title[:120])
		ax.text(0,-.25,global_param_title[120:240])

	if variable_time: 
		title = params['out_dir']+tstamp+'_timexpop_'+feat_name+'.png'
	else:
		title = params['out_dir']+tstamp+'_'+feat_name+'.png'
	plt.savefig(title)
	plt.clf()
	plt.close()
