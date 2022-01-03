import sys

from tasks import task1
from tasks import task2


_DATA = {
    'generator_data': 'data/generators.csv',
    'bus_data': 'data/buses.csv',
    'branch_data': 'data/branches.csv',
}

i = 0
j = 0
cost_data = []
extra_cost_data = []

while i < 1000:
    if j%2 == 0:
        cost = solve_task_extra('solutions/tasks3.txt',if_extra=False, write_solution=True,data=_DATA)
        cost_data.append(cost)
        j += 1
    else:
        cost = solve_task_extra('solutions/tasks3.txt',if_extra=True, write_solution=True,data=_DATA)
        extra_cost_data.append(cost)
        j += 1
    i += 1

# TODO: output extra cost

def solve_task_extra(filepath, if_extra=False, write_solution=True, **data):
    """Solve args-specified task and write solution to filepath. Return cost if running task 2."""

    if if_extra:
         # 1.Dheck which non-wind generators gammas == pmax
         id, pmax = [], []
         for generator in generators:
             if generator.fuel != "wind":
                 id.append(generator.generator)
                 pmax.append(generator.pmax)
        # gamma
        # 2. Double their pmax and update "generators.csv"

    model = task1.setup_model(**data) # TODO

    def solve(model):
        """Solve model and return solution string."""
        model.params.method = 2
        model.params.Crossover = 0
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
    return task2.compute_cost(solved_model, output_params=write_solution) if not data['task1'] else None


#run_task(sys.argv[1:])
