import os, math

def bool(x):
	if x in [0,'0','False',False,'false','unuh','noway','gtfofh']:
		return False
	elif x in [1,'1','True',True,'true','yeaya','fosho','nodoubt']:
		return True
	else:
		assert(False) # value cannot be evaluated as true or false

def rng(x):
    return range(len(x))

def avg(x):
	return sum(x)/len(x)

def avg_by_key(X,key):
	summ = 0
	for x in X:
		summ += x[key]
	return summ/len(x)

def var_by_key(X,key):
	varr = 0
	the_avg = avg_by_key(X,key)
	for x in X:
		varr += math.pow(the_avg-x[key],2)
	return math.pow(varr/len(x),1/2)

def var(x):
	the_avg = avg(x)
	var = avg([math.pow(the_avg-x[i],2) for i in rng(x)])
	return math.pow(var,1/2)

def L1(x):
	the_avg = avg(x)
	L1 = avg([abs(the_avg-x[i]) for i in rng(x)])
	return L1

def powavg(x,power):
	a = sum([math.pow(x[i],power) for i in range(len(x))])/len(x)
	return math.pow(a,1/power)


def check_build_dir(dirr):
    if not os.path.exists(dirr):
        print("\nCreating new directory for output at: " + str(dirr) + '\n')
        os.makedirs(dirr)

def sort_a_by_b(A,B,reverse=False):
	#naively sorts by min
	a,b=A.copy(), B.copy() #otherwise will change in place
	not_done, iters = True,0
	while not_done:
		not_done = False
		for i in range(len(b)-1):
			if b[i] < b[i+1]:
				b = swap(b,i, i+1)
				a = swap(a,i, i+1)
				not_done=True
		iters += 1
		if iters > 10000: assert(False)
	if reverse:
		a.reverse(), b.reverse()
	return a,b

def swap(array,i,j):
	z=array[i]
	array[i] = array[j]
	array[j] = z
	return array

def safe_div_array(A,B):
	# a is numerator, b is divisor
	assert(len(A) == len(B))
	z=[]
	for i in rng(A):
		if B[i] == 0: z+=[0]
		else: z+=[A[i]/B[i]]
	return z