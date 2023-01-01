#!python3
'''
In this example we use fairlens library's sensitive.detect_names method to
detect the sensitive columns in a dataframe or string list by creating
dictionary which maps the attribute names to the corresponding sensitive
category name (such as Gender, Religion etc). We have used both Shallow and
Deep Detection algorithm.
'''

import pandas as pd
import fairlens as fl
columns = ["native", "location", "house", "subscription", "salary", "religion", "score"]

#Sensitive Attribute Detection

df = pd.DataFrame(columns=columns)
fl.sensitive.detect_names_df(df)
columns = ["A", "B", "C", "Salary", "D", "Score"]
data = [
    ["male", "hearing impairment", "heterosexual", "50000", "christianity", "10"],
    ["female", "obsessive compulsive disorder", "asexual", "60000", "daoism", "10"],
]
df = pd.DataFrame(data, columns=columns)
fl.sensitive.detect_names_df(df)
fl.sensitive.detect_names_df(df, deep_search=True)
df = pd.read_csv("../data/compas.csv")
print(df.head())
# Apply shallow detection algorithm.
print("Shallow detection algo", fl.sensitive.detect_names_df(df))

df_deep = pd.read_csv("/Users/shachatt1/Desktop/sharmi/books/My_book_responsible_ai/python_code/Chapter5/fairlens-main/datasets/compas.csv")
df_deep = df_deep.rename(columns={"Ethnicity": "A", "Language": "Random", "MaritalStatus": "B", "Sex": "C"})
# Apply deep detection algorithm.
print("Deep detection algorithm", fl.sensitive.detect_names_df(df, deep_search=True))

