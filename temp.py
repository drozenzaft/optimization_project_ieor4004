

# Shapiro-Wilk Test
from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro
import numpy as np
import pylab
import scipy.stats as stats
import seaborn as sns
import math
import scipy
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import weibull_max


with open('tasks/solutions/costs.txt') as f:
    costs = f.read()
cost_list = [float(c) for c in costs.strip('][').split(',')]  # 1000 costs
cost_list = np.array(cost_list)

# remove the outlier
cost_list = cost_list[cost_list>5000000]  # remaining 998
#cost_log = [math.log(c) for c in cost_list]

# 1. Quantile-Quantile Plot
stats.probplot(cost_list, dist="norm", plot=pylab)

# 2. Box Plot
ax = sns.boxplot(x=cost_list)

# 3. Shapiro-Wilk Test
stat,p = shapiro(cost_list)
if p>0.05:
    print('probably guassian')
else:
    print('not gaussian')



def check_distribution(y_std):
    chi_square_statistics = []
    # 11 equi-distant bins of observed Data
    percentile_bins = np.linspace(0, 100, 11)
    percentile_cutoffs = np.percentile(y_std, percentile_bins)
    observed_frequency, bins = (np.histogram(y_std, bins=percentile_cutoffs))
    cum_observed_frequency = np.cumsum(observed_frequency)
    dist_names = ['weibull_min', 'norm', 'weibull_max', 'beta','invgauss', 'uniform', 'gamma', 'expon','lognorm',
                  'pearson3','triang']
    # Loop through candidate distributions
    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(scipy.stats, distribution)
        param = dist.fit(y_std)
        print("{}\n{}\n".format(dist, param))
        # Get expected counts in percentile bins
        # cdf of fitted sistrinution across bins
        cdf_fitted = dist.cdf(percentile_cutoffs, *param)
        expected_frequency = []
        for bin in range(len(percentile_bins) - 1):
            expected_cdf_area = cdf_fitted[bin + 1] - cdf_fitted[bin]
            expected_frequency.append(expected_cdf_area)
        # Chi-square Statistics
        expected_frequency = np.array(expected_frequency) * 2
        cum_expected_frequency = np.cumsum(expected_frequency)
        ss = sum(((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency)
        chi_square_statistics.append(ss)
    # Sort by minimum ch-square statistics
    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['chi_square'] = chi_square_statistics
    results.sort_values(['chi_square'], inplace=True)

    print('\nDistributions listed by Betterment of fit:')
    print('............................................')
    print(results)

check_distribution(cost_list)

