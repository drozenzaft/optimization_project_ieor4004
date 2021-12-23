"""Task 2 functions."""
import numpy as np
from numpy.random import default_rng
import pandas as pd

from classes.generator import load_generators


# def print_dual(model, filepath):
#     """[UNUSED] Write the dual to a file using the solved model in task 1."""
#     printed_dual = ''
#     for c in model.getConstrs():
#         printed_dual += f'dual for {c.constrname} = {c.pi}\n'
#     with open(filepath, 'w', encoding='utf-8') as f:
#         f.write(printed_dual)
#         print(f'Wrote dual solution at {filepath}\n')


def get_cov_matrix(cov_data='data/scaledcov.txt'):
    """Load covariance matrix from data file."""
    return pd.read_csv(cov_data, sep=' ', header=None).dropna(how='all', axis=1, inplace=False)


def randomize_gammas(pmax, cov):
    """Generate MVN distribution using optimized gammas."""
    mvn = default_rng().multivariate_normal(pmax, cov)
    return np.where(mvn < 0, 0, mvn)  # replace negatives with 0


def produce_gammas(n=1000):
    """Repeat gamma randomization n times."""
    wind_generators = load_generators(wind_filter=True)
    pmax = [wind_generator.pmax for wind_generator in wind_generators]
    cov = get_cov_matrix()
    return [randomize_gammas(pmax, cov) for _ in range(n)]


def print_gammas(gammas, filename='tasks/solutions/gammas.txt'):
    """Write gammas to a file."""
    with open(filename, 'w', encoding='utf-8') as f:
        np.savetxt(f, gammas)
        print(f'Wrote gammas to file {filename}\n')


def get_costs(duals):
    """Given the dual variables for the bus constraints, compute the cost."""
    # Write this later
    pass
