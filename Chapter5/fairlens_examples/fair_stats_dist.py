import pandas as pd
import fairlens as fl
import numpy as np

df = pd.read_csv("../data/compas.csv")
df.info()
target_attr = "RawScore"
# x = df[df["Ethnicity"] == "African-American"][target_attr]
# y = df[df["Ethnicity"] == "Caucasian"][target_attr]
#
# #Compute Statistical Distances
# fl.metrics.KolmogorovSmirnovDistance()(x, y)
# _, bin_edges = np.histogram(df[target_attr], bins="auto")
#
# fl.metrics.EarthMoversDistance(bin_edges)(x, y)
# ord = 1
# fl.metrics.Norm(ord=ord)(x, y)
group1 = {"Ethnicity": ["African-American"]}
group2 = df["Ethnicity"] == "Caucasian"
print(fl.metrics.stat_distance(df, target_attr, group1, group2, mode="auto"))
print(fl.metrics.stat_distance(df, target_attr, group1, group2, mode="auto", p_value=True))
_, bin_edges = np.histogram(df[target_attr], bins="auto")
print(fl.metrics.stat_distance(df, target_attr, group1, group2, mode="emd", bin_edges=bin_edges))