#!python3
'''
In this example we use fairlens library's FairnessScorer to generate a fairness report on a dataset,
provided a target column, which here is the 'RawScore' .
Here the target column stays independent of the sensitive attributes.
'''


import pandas as pd
import fairlens as fl
df = pd.read_csv("../data/compas.csv")
#Generate report
print(df.info())
fscorer = fl.FairnessScorer(df, "RawScore", ["Ethnicity", "Sex"])
fscorer.plot_distributions()
#Demographic report
print("Demo Rep", fscorer.demographic_report())
#print("Demo Rep dis_rest", fscorer.demographic_report(method="dist_to_rest"))

#Scoring API
sensitive_attrs = ["Ethnicity", "Sex"]
target_attr = "RawScore"
fscorer = fl.FairnessScorer(df, target_attr, sensitive_attrs)
df_dist = fscorer.distribution_score()
print("Scores", df_dist)
