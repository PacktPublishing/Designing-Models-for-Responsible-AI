import pandas as pd

df = pd.read_csv("../../data/german_credit_data.csv")
data = df[['Age', 'Sex', 'Job', 'Duration', 'Credit amount']]
data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})

covar_sex_dur = data.Sex.cov(data.Duration)
variance_sex = data.Sex.var()
variance_dur= data.Duration.var()
association =covar_sex_dur/(variance_sex*variance_dur)
print("Association between Sex and Duration", association)
