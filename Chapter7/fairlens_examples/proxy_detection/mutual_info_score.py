#!python3
'''
In this example we try to detect presence of proxy features by determinig
similarity between two labels/variables of the same datasset. It mathematically
uses the below formula to determine :
the Mutual Information etween clusterings :math:`U` and :math:`V'

    MI(U,V)=\\sum_{i=1}^{|U|} \\sum_{j=1}^{|V|} \\frac{|U_i\\cap V_j|}{N}
    \\log\\frac{N|U_i \\cap V_j|}{|U_i||V_j|}

Here :math:`|U_i|` is the number of the samples
in cluster :math:`U_i` and :math:`|V_j|` is the number of the
samples in cluster :math:`V_j`.
'''

from sklearn.metrics import mutual_info_score
import pandas as pd

df = pd.read_csv("../../data/german_credit_data.csv")


data = df[['Age', 'Sex', 'Job', 'Duration', 'Credit amount']]


mi_1 = mutual_info_score(data['Age'], data['Sex'])
mi_2 = mutual_info_score(data['Job'], data['Sex'])
mi_3 = mutual_info_score(data['Duration'], data['Sex'])
mi_4 = mutual_info_score(data['Credit amount'], data['Sex'])

print("Mutual Info", mi_1, mi_2, mi_3, mi_4)