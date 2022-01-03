"""Task 1 LP solution."""
import gurobipy as grbpy

from classes.generator import load_generators
from classes.bus import load_buses
from classes.branch import load_branches
from tasks.task2 import produce_pmaxes


def setup_model(generator_data, bus_data, branch_data, task1=True, output_pmaxes=True):
    """Minimize objective (8) with respect to constraints (1), (2), (5), (6) and (7).
    Pass random_pmaxes argument to randomize pmaxes for Task 2."""

    generators, buses, branches = (
        load_generators(generator_data),
        load_buses(bus_data),
        load_branches(branch_data)
    )
    new_pmaxes = {} if task1 else produce_pmaxes(generators, output_pmaxes=output_pmaxes)  # generate random pmaxes for task 2
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
    gamma = {}
    new_gamma = {}
    bia = {}
    bib = {}
    for g in generators:
        ub = new_pmaxes[g.generator] if g.generator in new_pmaxes else g.pmax  # set upper bound based on mvn sample for task 2
        gamma[g.generator] = model.addVar(name=f'Γ{g.generator}', lb=0, ub=ub)  # add gamma to model wrt constraint (5)
        new_gamma[g.generator] = model.addVar(name=f'Γ{g.generator}', lb=0, ub=2*ub) #case when expanded
        if g.fuel != 'wind':
            bin_ia = model.addVar(vtype=grbpy.GRB.BINARY,name=f'exa{g.generator}') # add binary_a for each generator
            bin_ib = model.addVar(vtype=grbpy.GRB.BINARY,name=f'exb{g.generator}')
            bia[g.generator] = bin_ia
            bib[g.generator] = bin_ib
            constr_expanded = bin_ia + bin_ib <= 1 
            model.addConstr(constr_expanded, f'constr_expanded')
            obj += bin_ib*(g.sigma * gamma[g.generator]) +bin_ia*(g.sigma * new_gamma[g.generator]) # update objective function for each generator
            obj += g.sigma /10 * bin_ia
        else:
            obj += g.sigma * gamma[g.generator]
    constr_binary = sum(bia.values()) <= 10
    model.addConstr(constr_binary, f'constr_binary')
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
        l = []
        for generator in G_i:
            if generator.fuel == 'wind':
                l.append(gamma[generator.generator])
            else:
                l.append(bib[generator.generator]*gamma[generator.generator] + bia[generator.generator]*new_gamma[generator.generator])
        constr6_rhs = sum(l) - (i.load - S[i.bus])
        constr6 = constr6_lhs == constr6_rhs
        model.addConstr(constr6, f'constr6 dual for bus {i.bus}')

        obj += (10 ** 6) * S[i.bus]  # update objective function for each bus

    model.setObjective(obj, grbpy.GRB.MINIMIZE)
    return model
