
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

bins=40
hist, edges = np.histogram(cost_list, bins)
x = np.linspace(min(cost_list),max(cost_list),bins)

# frequency plot
y = [float(h)/np.size(cost_list) for h in hist]
plt.scatter(x,y)

# fit normal distribution
#mu, sigma = scipy.stats.norm.fit(cost_list)
#fitted_data = scipy.stats.distributions.norm.pdf(x,mu,sigma)
#scale_param = 1000
#plt.plot(x, scale_param*stats.norm.pdf(x, mu, sigma), color='red')
#plt.savefig('tasks/solutions/cost_distribution.png')

# Calculate VAR
#Z95 = 1.96
#VAR = Z95*sigma + mu

a, loc, scale = scipy.stats.lognorm.fit(cost_list)
fitted_data = scipy.stats.lognorm.pdf(x, a, loc, scale)
scale_param = 70000/bins
plt.plot(x, scale_param*fitted_data, color='red')
#plt.savefig('solutions/cost_distribution.png')

#Calculate VAR
print("\nThe VAR at 95 percent confidence is ", stats.lognorm.ppf(0.95, a, loc, scale),"\n")


