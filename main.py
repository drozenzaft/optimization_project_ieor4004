import sys

from tasks import task1
from tasks import task2

from classes.generator import load_generators
from classes.bus import load_buses
from classes.branch import load_branches


_DATA = {
    'generator_data': 'data/generators.csv',
    'bus_data': 'data/buses.csv',
    'branch_data': 'data/branches.csv',
}


def run_task(args, output_pmaxes=True, data=_DATA):
    """Get task from runtime args."""
    if args:
        if '1' in args[0]:
            task = '1'
        elif '2' in args[0]:
            task = '2'
        elif '3' in args[0]:
            task = '3'

    is_task1 = True if task == '1' else False
    filepath = f'tasks/solutions/task{task}.txt'

    data['task1'] = is_task1
    data['task'] = task
    data['output_pmaxes'] = output_pmaxes

    if is_task1:
        solve_task(filepath, **data)
        return

    write_solution, cost_data = False, []
    i = 0
    while i < 10:  # run task2 or task3 1000 times if selected
        if i == 0:
            write_solution = True  # write first solution to file
        elif i == 1:
            write_solution = False
        cost = solve_task(filepath, write_solution=write_solution, **data)
        cost_data.append(cost)
        print(i)
        i += 1
    print(f'Wrote pmaxes at tasks/solutions/pmaxes.txt\n') if output_pmaxes else None

    with open('tasks/solutions/costs.txt', 'w', encoding='utf-8') as f:  # write costs to file
        f.write(str(cost_data))
        print('Wrote costs at tasks/solutions/costs.txt\n')
    task2.plot_costs(cost_data)


def solve_task(filepath, write_solution=True, **data):
    """Solve args-specified task and write solution to filepath. Return cost if running task 2."""
    generators, buses, branches = (
        load_generators(data['generator_data']),
        load_buses(data['bus_data']),
        load_branches(data['branch_data'])
    )
    model, pmaxes = task1.setup_model(generators, buses, branches, task1=data['task1'], output_pmaxes=data['output_pmaxes'])

    def solve(model):
        """Solve model and return solution string."""
        if not data['task1']:
            model.params.method = 2
            model.params.Crossover = 0
        model.optimize()

        if data['task1']:
            solution = f'Optimal Objective Value: {model.getObjective().getValue()}\n'
            for v in model.getVars():
                solution += f'{v.varname} = {v.x}\n'
            new_generators = {}
        else:
            new_generators, solution = extract_capped_generators(model, pmaxes)
        return model, solution, new_generators

    solved_model, solution, new_generators = solve(model)

    def solve_task3():
        """Solve task 3."""
        task3_model, pmaxes = task1.setup_model(new_generators, buses, branches, task1=False, output_pmaxes=data['output_pmaxes'])
        solved_task3_model, task3_solution, new_task3_generators = solve(task3_model)
        with open('tasks/solutions/task3.txt', 'w', encoding='utf-8') as f:
            f.write(solution)
            print(f'\nWrote solution to task3 at tasks/solutions/task3.txt\n')
        return task2.compute_cost(solved_task3_model, output_params=write_solution)
    if data['task'] == '3':
        return solve_task3()


    if write_solution:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(solution)
            task_name = filepath[-9:-4]
            print(f'\nWrote solution to {task_name} at {filepath}\n')
    return task2.compute_cost(solved_model, output_params=write_solution) if not data['task1'] else None


def extract_capped_generators(solved_model, new_pmaxes):
    """Extract capped-out non-wind generators from solved model and return new generator set."""
    solution = f'Optimal Objective Value: {solved_model.getObjective().getValue()}\n'
    # print(f'new pmaxes:\n\n{new_pmaxes}')
    generators = load_generators()
    gammas = {}
    for v in solved_model.getVars():
        solution += f'{v.varname} = {v.x}\n'
        if v.varname[0] == 'Γ':
            generator_id = int(v.varname[1:])
            gammas[generator_id] = v.x
    for generator in generators:
        if generator.fuel != 'wind' and abs(gammas[generator_id] - generator.pmax) <= 10 ** -1:  # set tolerance for capped generator value
            generator.pmax *= 2
            print(f'Doubled pmax value for generator {generator.generator}')
            print(f'New pmax value is {generator.pmax}')
        elif generator.fuel == 'wind':
            generator.pmax = new_pmaxes[generator.generator]
    return generators, solution




run_task(sys.argv[1:])
