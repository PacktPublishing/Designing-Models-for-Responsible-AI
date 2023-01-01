#!python3
'''
In this example we use fairlens library's FairnessScorer to generate a fairness report on a dataset,
provided a target column, which here is the 'RawScore' .
Here the target column stays independent of the sensitive attributes.
'''

import pandas as pd
import fairlens as fl

df = pd.read_csv("../data/compas.csv")
df.info()
fscorer = fl.FairnessScorer(df, "RawScore")
print(fscorer.sensitive_attrs)
fscorer.plot_distributions()

fscorer = fl.FairnessScorer(df, "RawScore", ["Ethnicity", "Sex", "MaritalStatus"])
fscorer.demographic_report(max_rows=20)