import pandas as pd
import fairlens as fl

df = pd.read_csv("../data/compas.csv")
df.info()
fscorer = fl.FairnessScorer(df, "RawScore")
print(fscorer.sensitive_attrs)
fscorer.plot_distributions()

fscorer = fl.FairnessScorer(df, "RawScore", ["Ethnicity", "Sex", "MaritalStatus"])
fscorer.demographic_report(max_rows=20)