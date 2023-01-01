#!python3
'''
In this example we use fairlens library's find_sensitive_correlations method to
evaluate the columns that are not considered to be immediately sensitive and finds if any is strongly
correlated with a sensitive column. It then specifies both the sensitive column name and the
sensitive category it is a part of.
'''


import pandas as pd

import fairlens as fl
from fairlens.metrics import distance_nn_correlation, distance_cn_correlation, cramers_v

#Detect Hidden Correlations
columns = ["gender", "random", "score"]
data = [["male", 10, 50], ["female", 20, 80], ["male", 20, 60], ["female", 10, 90]]
df = pd.DataFrame(data, columns=columns)

#Sensitive Proxy Detection
print(fl.sensitive.find_sensitive_correlations(df))

col_names = ["gender", "nationality", "random", "corr1", "corr2"]

data = [
    ["woman", "spanish", 715, 10, 20],
    ["man", "spanish", 1008, 20, 20],
    ["man", "french", 932, 20, 10],
    ["woman", "french", 1300, 10, 10],
]

df = pd.DataFrame(data, columns=col_names)
print(fl.sensitive.find_sensitive_correlations(df))

#Correlation Heatmaps

# df = pd.read_csv("../data/german_credit_data.csv")
# fl.plot.two_column_heatmap(df, distance_nn_correlation, distance_cn_correlation, cramers_v)

