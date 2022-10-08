import numpy as np

from lightfm.datasets import fetch_movielens

movielens = fetch_movielens()



import scipy.stats
import numpy as np

data1 = scipy.stats.norm.rvs(size=100000, loc=0, scale=1.5, random_state=123)
hist1 = np.histogram(data1, bins=100)
hist1_dist = scipy.stats.rv_histogram(hist1)
import matplotlib.pyplot as plt
X1 = np.linspace(-8.0, -2.0, 1000)
plt.title("PDF")
plt.hist(data1, density=True, bins=100,  color ='blue')
plt.plot(X1, hist1_dist.pdf(X1), label='PDF', color = 'blue')

data2 = scipy.stats.norm.rvs(size=100000, loc=0, scale=5.5, random_state=123)
hist2 = np.histogram(data2, bins=100)
hist2_dist = scipy.stats.rv_histogram(hist2)
X2 = np.linspace(4.0, 8.0, 1000)
plt.title("Probability Density Function")
plt.hist(data2, density=True, bins=100, color ='green')
plt.plot(X2, hist2_dist.pdf(X2), label='PDF', color = 'green')
plt.legend(['X1', 'X2'])
#plt.plot(X, hist_dist.cdf(X), label='CDF')
plt.show()

kl_div = scipy.stats.entropy(X1, X2, base=2)
print("KL div X1 and X2", kl_div)

Y1 = hist1_dist.pdf(X1)
Y2 = hist2_dist.pdf(X2)

# Obtain point-wise mean of the two PDFs Y1 and Y2, denote it as M
M = (Y1 + Y2) / 2
# Compute Kullback-Leibler divergence between Y1 and M
d1 = scipy.stats.entropy(Y1, M, base=2)
print("KL div Y1 and M", d1)
# Compute Kullback-Leibler divergence between Y2 and M
d2 = scipy.stats.entropy(Y2, M, base=2)
print("KL div Y2 and M", d2)
# Take the average of d1 and d2
# we get the symmetric Jensen-Shanon divergence
js_dv = (d1 + d2) / 2
# Jensen-Shanon distance is the square root of the JS divergence
js_distance = np.sqrt(js_dv)
print("JS Dist d1 and d2", js_distance)

#Evaluate against scipy's calculation
js_distance_scipy = scipy.spatial.distance.jensenshannon(Y1, Y2)
print("JS Dist d1 and d2 of Scipy", js_distance_scipy)

js_distance_scipy = scipy.spatial.distance.jensenshannon(X1, X2)
print("JS Dist X1 and X2 of Scipy", js_distance_scipy)

dx1 = scipy.stats.entropy(Y1, X1, base=2)
dx2 = scipy.stats.entropy(Y2, X2, base=2)
js_dv = (dx1 + dx2) / 2
print("JS Div dx1 and dx2", js_dv)