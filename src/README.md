usage: main.py

In order to launch simulations, you should change parameters in `params.txt`.

Parameters names are in the first column and their meaning (and available options) is explained in the last column.
The second column contains actual values of the parameter. If you want to launch several types of simulation and plot
them on the same image, you should use square brackets and list the parameners inside (cf. for example, mutation_rate)
and put `1` instead of `0` to the fourth column. (NB: you should list all combination of the parameters).
The third column contains the type of a parameter (`int`, `float`, `str`, `bool`).

To run the simulation, use

```
python main.py
```
The plots will be in the output folder.

Notes:
- make an output directory corresponding to the output_dir param! 
- note that param.txt must be TAB delimited. Issues parsing often related to automated spaces instead of tabs.