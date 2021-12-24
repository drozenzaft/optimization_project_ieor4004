"""Task 2 functions."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from classes.bus import load_buses


def get_cov_matrix(cov_data='data/scaledcov.txt'):
    """Load covariance matrix from data file."""
    return pd.read_csv(cov_data, sep=' ', header=None).dropna(how='all', axis=1, inplace=False)


def randomize_gammas(pmax, cov):
    """Generate MVN distribution using optimized gammas."""
    mvn = np.random.default_rng().multivariate_normal(pmax, cov)
    return np.where(mvn < 0, 0, mvn)  # replace negatives with 0


def produce_gammas(generators, output_gammas=False):
    """Produce gammas according to generator parameters and return a dictionary in the form {generator_i.generator: gamma_i}."""
    id, pmax = [], []
    for generator in generators:
        id.append(generator.generator)
        pmax.append(generator.pmax)
    cov = get_cov_matrix()
    gammas = randomize_gammas(pmax, cov)
    write_gammas(gammas) if output_gammas else None
    return dict(zip(id, gammas))


def write_gammas(gammas, filename='tasks/solutions/gammas.txt'):
    """Write gammas to a file."""
    with open(filename, 'a', encoding='utf-8') as f:
        np.savetxt(f, gammas)


def compute_cost(solved_model):
    """Given a solved model, use the bus dataset to compute the cost."""
    # Write this later
    vars = solved_model.getVars()
    buses = load_buses()

    # build out π dictionary in form {bus_id: dual_value} - split to extract bus_id from constrname
    π = {int(c.constrname.split(' ')[-1]): c.pi for c in solved_model.getConstrs() if c.constrname[6] == '6'}
    S = {int(v.varname[1:]): v.x for v in vars if v.varname[0] == 'S'}  # slice varname to exclude 'S'

    cost = 0
    for i in buses:
        π_i = -π[i.bus]
        d_i = i.load
        S_i = S[i.bus]
        cost += π_i * (d_i - S_i)
    return cost


def plot_costs(costs):
    """Plot cost distribution on a histogram."""
    plt.hist(costs)
    filename = 'tasks/solutions/costs_histogram.png'
    plt.savefig(filename)
    print(f"Saving cost distribution histogram to {filename}\n")
    plt.close()
