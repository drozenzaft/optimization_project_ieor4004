"""Task 1 LP solution."""
import gurobipy as grbpy

from classes.generator import load_generators
from classes.bus import load_buses
from classes.branch import load_branches
from tasks.task2 import produce_gammas


def setup_model(generator_data, bus_data, branch_data, task1=True, output_gammas=True):
    """Minimize objective (8) with respect to constraints (1), (2), (5), (6) and (7).
    Pass random_gammas argument to preset gammas for Task 2."""

    generators, buses, branches = (
        load_generators(dataset=generator_data, wind_filter=(not task1)),  # set wind filter for task 2
        load_buses(bus_data),
        load_branches(branch_data)
    )
    model, obj = grbpy.Model(), 0

    # set branch constraints (1) and (2)
    p, theta, added = {}, {}, set()
    for b in branches:
        # first create θ_i variables for constraint 1, using the "added" set to avoid duplicating model variables
        [theta.update({bus: model.addVar(name=f'θ{bus}')}) for bus in (b.from_bus, b.to_bus) if bus not in added and not added.add(bus)]
        p[b.branch] = model.addVar(name=f'p{b.branch}', lb=-b.u, ub=b.u)  # add p_b to model wrt constraint (2) bounds
        constr1 = p[b.branch] == (theta[b.from_bus] - theta[b.to_bus]) / b.x
        model.addConstr(constr1, f'constr1 dual for branch {b.branch}')

    # set generator constraint (5)
    gamma = {} if task1 else produce_gammas(generators, output_gammas=output_gammas)  # generate random gammas for task 2
    for g in generators:
        if task1:  # task 1 - add gammas to model for optimization
            gamma[g.generator] = model.addVar(name=f'Γ{g.generator}', lb=0, ub=g.pmax)  # task 1: add gamma to model wrt constraint (5)
        obj += g.sigma * gamma[g.generator]  # update objective function for each generator

    # set bus constraints (6) and (7)
    S = {}
    for i in buses:
        S[i.bus] = model.addVar(name=f'S{i.bus}', lb=0, ub=i.load)  # set S_i wrt constraint (7) bounds

        G_i = i.generators(generators)  # get G(i) set
        F_i, T_i = i.branches(branches)  # get F(i) and T(i) sets

        constr6_lhs = (
            sum([p[from_branch.branch] for from_branch in F_i])
            - sum([p[to_branch.branch] for to_branch in T_i])
        )
        constr6_rhs = sum([gamma[generator.generator] for generator in G_i]) - (i.load - S[i.bus])
        constr6 = constr6_lhs == constr6_rhs
        model.addConstr(constr6, f'constr6 dual for bus {i.bus}')

        obj += (10 ** 6) * S[i.bus]  # update objective function for each bus

    model.setObjective(obj, grbpy.GRB.MINIMIZE)
    return model
