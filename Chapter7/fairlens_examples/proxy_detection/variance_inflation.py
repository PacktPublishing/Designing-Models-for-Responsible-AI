#!python3
'''
In this example we demonstrate proxy detection through
the Variance Inflation Factor (VIF) metric that aims to measure multicollinearity
by evaluating coefficient of determination (R2), for each variable.
'''
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("../../data/german_credit_data.csv")
data = df[['Age', 'Sex', 'Job', 'Duration', 'Credit amount']]
data = data.dropna()

# creating dummies for gender
# the independent variables set

data['Sex'] = data['Sex'].map({'male': 0, 'female': 1})
X = data[['Age', 'Sex', 'Job', 'Credit amount', 'Duration']]

# VIF dataframe
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
# calculating VIF for each feature
vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                   for i in range(len(X.columns))]

print(vif_data)