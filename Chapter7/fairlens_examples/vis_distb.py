#!python3

'''
In this example we use fairlens library's plot.distr_plot method to
plot the distribution of the groups with respect to the target attribute,
which here is the RawScore.
'''

import pandas as pd
import fairlens as fl
import matplotlib.pyplot as plt

#Visualizing distributions

fl.plot.use_style()
df = pd.read_csv("../datasets/compas.csv")
print(df.info())

#Distribution of Groups

target_attr = "RawScore"
group1 = {"Sex": ["Male"], "Ethnicity": ["Caucasian"]}
group2 = {"Sex": ["Male"], "Ethnicity": ["African-American"]}

fl.plot.distr_plot(df, target_attr, [group1, group2])

#Distribution of Groups in a Column
target_attr = "RawScore"

sensitive_attr = "Ethnicity"

fl.plot.attr_distr_plot(df, target_attr, sensitive_attr)
target_attr = "RawScore"

sensitive_attrs = ["Ethnicity", "Sex"]

fl.plot.mult_distr_plot(df, target_attr, sensitive_attrs)
