import init, run,plot

# for the lazy: cd Goo*/*M2/*S2/Heuristics/heur*/src

# TODO: add variance as variance in solutions
# workflow: plots w/o dyn params justify which params are best in static case
# then use those for comparison against dyn, since dyn will use diff starting values


param_file = './params.txt'
batch_params, global_param_title = init.batch_params(param_file)
features = run.batch(batch_params)

plot.solvers_x_features(features, batch_params['global'], global_param_title)
print("\nDone.\n")

