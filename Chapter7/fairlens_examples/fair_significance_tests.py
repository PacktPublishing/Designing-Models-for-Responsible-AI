#!python3
'''
In this example we use fairlens library's permutation_statistic metric that runs a hypothesis test
to demonstrate that a model is fair across two groups with respect to any given metric.
In addition we have also used bootstrap_statistic to setup the hypothesis test to determine fairness
between groups through a resampling technique on a population by sampling a dataset with replacement.
'''


import pandas as pd

import fairlens as fl

df = pd.read_csv("../data/compas.csv")
group1 = df[df["Sex"] == "Male"]["RawScore"]
group2 = df[df["Sex"] == "Female"]["RawScore"]

#Resampling
test_statistic = lambda x, y: x.mean() - y.mean()
t_distribution = fl.metrics.permutation_statistic(group1, group2, test_statistic, n_perm=100)
print("Tdistb", t_distribution)
t_distribution = fl.metrics.bootstrap_statistic(group1, group2, test_statistic, n_samples=100)
print(t_distribution)

#Intervals and P-Values
t_observed = test_statistic(group1, group2)
print("Resampling Interval", fl.metrics.resampling_interval(t_observed, t_distribution, cl=0.95))
print("Resampling Pval", fl.metrics.resampling_p_value(t_observed, t_distribution, alternative="two-sided"))
