'''
In this example we learn about ADWIN (ADaptive WINdowing) drift detection mechanism. Adaptive sliding window algorithm is used for detecting change,
and keeping updated statistics about a data stream, thus allowing algorithms for drifting data, to be resistant to this phenomenon.

The general idea is to keep statistics from a window of variable size while detecting concept drift.
The algorithm will decide the size of the window by cutting the statistics’ window at different points and
analysing the average of some statistic over these two windows. If the absolute value of the difference between
the two averages surpasses a pre-defined threshold, change is detected at that point and all data before that time is discarded.
'''

from river import drift
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec

#refr https://deepchecks.com/how-to-detect-concept-drift-with-machine-learning-monitoring/

from alibi_detect.cd.preprocess import UAE, HiddenOutput


# Generate data for 3 distributions
random_state = np.random.RandomState(seed=42)
dist_a = random_state.normal(0.8, 0.05, 1000)
dist_b = random_state.normal(0.4, 0.02, 1000)
dist_c = random_state.normal(0.6, 0.1, 1000)

# Concatenate data to simulate a data stream with 2 drifts
stream = np.concatenate((dist_a, dist_b, dist_c))

# Auxiliary function to plot the data
def plot_data(dist_a, dist_b, dist_c, drifts=None):
   fig = plt.figure(figsize=(7,3), tight_layout=True)
   gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
   ax1, ax2 = plt.subplot(gs[0]), plt.subplot(gs[1])
   ax1.grid()
   ax1.plot(stream, label='Stream')
   ax2.grid(axis='y')
   ax2.hist(dist_a, label=r'$dist_a$')
   ax2.hist(dist_b, label=r'$dist_b$')
   ax2.hist(dist_c, label=r'$dist_c$')
   if drifts is not None:
       for drift_detected in drifts:
           ax1.axvline(drift_detected, color='red')
   plt.show()

plot_data(dist_a, dist_b, dist_c)

drift_detector = drift.ADWIN()
drifts = []

for i, val in enumerate(stream):
   drift_detector.update(val)   # Data is processed one sample at a time
   if drift_detector.change_detected:
       # The drift detector indicates after each sample if there is a drift in the data
       print(f'Change detected at index {i}')
       drifts.append(i)
       drift_detector.reset()   # As a best practice, we reset the detector

plot_data(dist_a, dist_b, dist_c, drifts)


#
# drift_detector = drift.HDDM_A()
# drifts = []
#
# for i, val in enumerate(stream):
#    drift_detector.update(val)   # Data is processed one sample at a time
#    if drift_detector.change_detected:
#        # The drift detector indicates after each sample if there is a drift in the data
#        print(f'Change detected at index {i}')
#        drifts.append(i)
#        drift_detector.reset()   # As a best practice, we reset the detector
#
# plot_data(dist_a, dist_b, dist_c, drifts)
#
