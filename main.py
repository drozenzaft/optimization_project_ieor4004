import sys

from tasks import task1


TASK1_DATA = {
    'generator_data': 'data/generators.csv',
    'bus_data': 'data/buses.csv',
    'branch_data': 'data/branches.csv'
}


def run_task(args, data=TASK1_DATA):
    """Get task from runtime args."""
    if len(args) >= 1 and '1' in args[0]:
        solve_task(task1, 'tasks/solutions/task1.txt', **data)
    else:  # will adjust this block for task 2 once complete
        print('\nRequested task not found. Solving Task 1 by default.\n')
        solve_task(task1, 'tasks/solutions/task1.txt', **data)


def solve_task(task, filepath, **data):
    """Solve task and write solution to filepath."""
    model = task.setup_model(**data)

    def solve(model):
        """Solve model and return solution string."""
        model.optimize()
        solution = f'Optimal Objective Value: {model.getObjective().getValue()}\n'
        for v in model.getVars():
            solution += f'{v.varname} = {v.x}\n'
        return solution

    solution = solve(model)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(solution)
        print(f'\nWrote solution to {task1.__name__} at {filepath}\n')


run_task(sys.argv[1:])
