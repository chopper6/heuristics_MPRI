from util import *


def batch_params(param_file):
	# EXPECT A TAB DELITED FILE: name\tvalue\dtype\batch
	if not os.path.isfile(param_file):
		assert(False) # unknown file
	with open(param_file) as pfile:
		lines = pfile.readlines()
		pdict, batch_dict = {},{} # PARAMS
		for line in lines[1:]: #skip header line
			if not line[0].isspace(): #skip if first char is whitespace
				param = line.strip().split('\t')
				if bool(param[3]): #if batch
					pieces = param[1].strip('[').strip(']').split(',') #should be list
					vals = [typecast(pieces[i],param[2]) for i in range(len(pieces))]
					batch_dict[param[0]] = vals 

				else: # static, not batch
					val = typecast(param[1],param[2])
					pdict[param[0]] = val

	lng = 0
	for b in batch_dict.keys():
		if lng == 0: lng=len(batch_dict[b])
		else: assert(len(batch_dict[b])==lng) #all batch params must be same length!
	
	batch_params={}
	batch_params['global'] = pdict.copy() #params that all runs share

	params_list = '' # will add this to image file names
	for k in batch_params['global'].keys():
		if k != "out_dir":
			params_list +=  ', ' + str(k) + '=' + str(batch_params['global'][k])


	for l in range(lng):
		params,title = pdict.copy(),''
		j=0
		for b in batch_dict.keys():
			if j >0: title += ', '
			params[b]=batch_dict[b][l]
			title += str(b)+':'+str(batch_dict[b][l])
			j+=1
		batch_params[title]=params


	return batch_params, params_list

def typecast(s,dtype):
	if dtype in ['str','string']:
		val = s
	elif dtype == 'int':
		val = int(s)
	elif dtype == 'float':
		val = float(s)
	elif dtype == 'bool':
		val = bool(s)
	else: assert(False) #unknown val
	return val