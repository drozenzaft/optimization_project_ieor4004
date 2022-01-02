

from scipy.stats import shapiro
import numpy as np
import scipy.stats as stats
import scipy
import matplotlib.pyplot as plt

with open('tasks/solutions/costs.txt') as f:
    costs = f.read()
cost_list = [float(c) for c in costs.strip('][').split(',')]  # 1000 costs
cost_list = np.array(cost_list)

# remove the outliers
cost_list = cost_list[cost_list>5000000]  # remaining 998

# histcounts
hist, edges = np.histogram(cost_list, bins=100)
#_, bins, _ = plt.hist(cost_list, bins=100, normed=True, alpha=0.5)
x = np.linspace(min(cost_list),max(cost_list),100)

# frequency plot
y = [h/998 for h in hist]
plt.scatter(x,y)

# fit normal distribution
mu, sigma = scipy.stats.norm.fit(cost_list)
fitted_data = scipy.stats.distributions.norm.pdf(x,mu,sigma)
scale_param = 500
plt.plot(x, scale_param*stats.norm.pdf(x, mu, sigma), color='red')

# Calculate VAR
Z95 = 1.96
VAR = Z95*sigma + mu