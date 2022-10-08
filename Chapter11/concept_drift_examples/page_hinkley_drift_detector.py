import random
from river import drift
import matplotlib.pyplot as plt
import numpy as np


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