from sklearn.metrics import mutual_info_score
import pandas as pd

df = pd.read_csv("../../data/german_credit_data.csv")


data = df[['Age', 'Sex', 'Job', 'Duration', 'Credit amount']]


mi_1 = mutual_info_score(data['Age'], data['Sex'])
mi_2 = mutual_info_score(data['Job'], data['Sex'])
mi_3 = mutual_info_score(data['Duration'], data['Sex'])
mi_4 = mutual_info_score(data['Credit amount'], data['Sex'])

print("Mutual Info", mi_1, mi_2, mi_3, mi_4)