import init, run,plot

# for the lazy: cd Documents/*M2/*S2/Heuristics/proj*/src

# general notes: 
# should organize which attributes a population P is expected to have somewhere

param_file = './params.txt'
batch_params = init.batch_params(param_file)
features = run.batch(batch_params)
plot.solvers_x_features(features, batch_params['global'])
print("\nDone.\n")

