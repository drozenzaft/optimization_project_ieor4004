"""Task 2 functions."""
import numpy as np
import pandas as pd


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


def get_costs(duals):
    """Given the dual variables for the bus constraints, compute the cost."""
    # Write this later
    pass
