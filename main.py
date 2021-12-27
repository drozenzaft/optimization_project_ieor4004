import sys

from tasks import task1
from tasks import task2


_DATA = {
    'generator_data': 'data/generators.csv',
    'bus_data': 'data/buses.csv',
    'branch_data': 'data/branches.csv',
}


def run_task(args, output_pmaxes=True, data=_DATA):
    """Get task from runtime args."""
    task = '2' if (args and '2' in args[0]) else '1'
    is_task1 = True if task == '1' else False
    filepath = f'tasks/solutions/task{task}.txt'

    data['task1'] = is_task1
    data['output_pmaxes'] = output_pmaxes

    if is_task1:
        solve_task(filepath, **data)
        return

    write_solution, cost_data = False, []
    i = 0
    while i < 1000:  # run task2 1000 times if selected
        if i == 0:
            write_solution = True  # Write last solution to file
        elif i == 1:
            write_solution = False
        try:
            cost = solve_task(filepath, write_solution=write_solution, **data)
            i += 1
        except AttributeError:
            print(f'Ran into infeasible LP after iteration {i}')
        cost_data.append(cost)
    print(f'Wrote pmaxes at tasks/solutions/pmaxes.txt\n') if output_pmaxes else None

    with open('tasks/solutions/costs.txt', 'w', encoding='utf-8') as f:  # write costs to file
        f.write(str(cost_data))
        print('Wrote costs at tasks/solutions/costs.txt\n')
    task2.plot_costs(cost_data)


def solve_task(filepath, write_solution=True, **data):
    """Solve args-specified task and write solution to filepath. Return cost if running task 2."""
    model = task1.setup_model(**data)

    def solve(model):
        """Solve model and return solution string."""
        model.optimize()
        solution = f'Optimal Objective Value: {model.getObjective().getValue()}\n'
        for v in model.getVars():
            solution += f'{v.varname} = {v.x}\n'
        return model, solution

    solved_model, solution = solve(model)
    if write_solution:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(solution)
            task_name = filepath[-9:-4]
            print(f'\nWrote solution to {task_name} at {filepath}\n')
    return task2.compute_cost(solved_model) if not data['task1'] else None


run_task(sys.argv[1:])
