'''
In this example we learn about PageHinkley drift detection technique. This change detection method
is responsible for computing the observed values and their mean up to the current moment. It signals a
concept drift if the observed mean at some instant is greater then a threshold value lambda.

'''

import random
from river import drift
import matplotlib.pyplot as plt


rng = random.Random(123456)
ph = drift.PageHinkley()

# Compose a data stream composed by three data distributions
data_stream = rng.choices([50, 100], k=1200) + rng.choices(range(600, 900), k=5000) + rng.choices(range(200, 300), k=5000)
plt.plot(data_stream)
plt.show()

# Update drift detector and verify if change is detected
for i, val in enumerate(data_stream):
    in_drift, _ = ph.update(val)
    if in_drift:
        print(f"Change detected at index {i}, input value: {val}")