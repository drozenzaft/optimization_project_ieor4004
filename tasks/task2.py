"""Task 2 functions."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from classes.bus import load_buses
from classes.generator import load_generators


def get_cov_matrix(cov_data='data/scaledcov.txt'):
    """Load covariance matrix from data file."""
    return pd.read_csv(cov_data, sep=' ', header=None).dropna(how='all', axis=1, inplace=False)


def randomize_pmaxes(pmax, cov):
    """Generate MVN distribution using pmax in dataset as mean."""
    mvn = np.random.default_rng().multivariate_normal(pmax, cov)
    return np.where(mvn < 0, 0, mvn)  # replace negatives with 0


def produce_pmaxes(generators, fuel='wind', task='2', output_pmaxes=True):
    """Produce random pmaxes for specified fuel (default wind) and return a dictionary in the form {generator_g.generator: pmax_g}."""
    id, pmax = [], []
    for generator in generators:
        if generator.fuel == fuel:
            id.append(generator.generator)
            pmax.append(generator.pmax)
    cov = get_cov_matrix()
    pmaxes = randomize_pmaxes(pmax, cov)
    write_pmaxes(pmaxes, task=task) if output_pmaxes else None
    return dict(zip(id, pmaxes))  # use a simpler object to reuse memory, better optimize code


def write_pmaxes(pmaxes, task='2'):  # write to memory map, or a binary file
    """Write pmaxes to a file."""
    filename = f'tasks/solutions/task{task}_pmaxes.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        np.savetxt(f, pmaxes)
        print(f'Wrote pmaxes at {filename}')


def compute_cost(solved_model, task='2', output_params=False):
    """Given a solved model, use the bus dataset to compute the cost."""
    vars = solved_model.getVars()
    generators = load_generators()
    buses = load_buses()

    if task == 'eec':
        gammas = {}
        new_gammas = {}
        expanded = []
        for v in vars:
            if v.varname[0] == 'Γ' and v.varname[1] != '_':
                generator_id = int(v.varname[1:])
                gammas[generator_id] = v.x
            if v.varname[1] == '_':
                generator_id = int(v.varname[5:])
                new_gammas[generator_id] = v.x
            if len(v.varname) > 2 and v.varname[2] == 'a':
                if v.x == 1:
                    generator_id = int(v.varname[3:])
                    expanded.append(generator_id)
        cost = 0
        for generator in generators:
            if generator.generator in expanded:
                cost += generator.sigma / 10 * generator.pmax
                if (new_gammas[generator.generator] - generator.pmax) > 1:  # set tolerance for capped generator value
                    cost += generator.sigma * generator.pmax + 4 * generator.sigma * (gammas[generator.generator] - generator.pmax) ** 2
                    if output_params:
                        print(f'expanding generator {generator.generator}')
                else:
                    cost += generator.sigma * generator.pmax
            else:
                if (gammas[generator.generator] - generator.pmax) > 1:  # set tolerance for capped generator value
                    cost += generator.sigma * generator.pmax + 4 * generator.sigma * (gammas[generator.generator] - generator.pmax) ** 2
                    if output_params:
                        print(f'expanding generator {generator.generator}')

    # build out π dictionary in form {bus_id: dual_value} - split to extract bus_id from constrname
    else:
        π = {int(c.constrname.split(' ')[-1]): c.pi for c in solved_model.getConstrs() if c.constrname[6] == '6'}
        S = {int(v.varname[1:]): v.x for v in vars if v.varname[0] == 'S'}  # slice varname to exclude 'S'
        if output_params:
            with open(f'tasks/solutions/task{task}_cost_params.txt', 'w', encoding='utf-8') as f:
                f.write(f'π dictionary:\n\n{π}\n\n\nS dictionary:\n\n{S}')
                print(f'\nWrote cost addends to tasks/solutions/task{task}_cost_params.txt\n')

        cost = 0
        for i in buses:
            π_i = -π[i.bus]
            d_i = i.load
            S_i = S[i.bus]
            cost += π_i * (d_i - S_i)
    return cost


def plot_costs(costs, filename='tasks/solutions/costs_histogram.png', task='2'):
    """Plot cost distribution on a histogram."""
    filename = f'tasks/solutions/task{task}_costs_histogram.png'
    if task == '2':
        filtered_costs = [i for i in costs if i >= 5000000]  # filter strange outliers (will investigate them in future)
    elif task == '3':
        filtered_costs = [i for i in costs if i >= 3750000]  # filter strange outliers (will investigate them in future)
    elif task == 'eec':
        filtered_costs = [i for i in costs if i >= 1000000]  # filter strange outliers (will investigate them in future)
    plt.hist(filtered_costs)
    plt.savefig(filename)
    print(f"Saving cost distribution histogram to {filename}\n")
    plt.close()
