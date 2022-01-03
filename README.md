# optimization_project_ieor4004
Final project for IEOR 4004 - Introduction to Optimization @ Columbia Engineering.

"The Optimizers" Roster:
- Alina Rodriguez
- Xueying Hu
- Sitong Zhong
- Daniel Rozenzaft
- Mars Dai


To run tasks:
- `python main.py [task]`
where task is either 1, 2, 3 (extra credit parts A and B), or eec (extra extra credit).

This will generate a solution file at `tasks/solutions/[task].txt`.


To generate cost distribution plots for tasks 2 and 3:
- `python main.py [task]`
where task is either 2 or 3.

This will generate a cost distribution plot at `tasks/solutions/[task]_cost_distribution.png`.


Language:
- Python 3.6+

Dependencies:
- [gurobipy package installation](https://pypi.org/project/gurobipy/)
- [Gurobi license](https://www.gurobi.com/academia/academic-program-and-licenses/)
- [numpy](https://pypi.org/project/numpy/)
- [pandas](https://pypi.org/project/pandas/)

Contents:
```
┌── README.md               # This document!
|
|── gurobi.env              # Configure Gurobi environment to suppress console output (solutions are stored in tasks/solutions)
|
├── tasks                   # Task models and solutions
|   ├── solutions           # Task solutions and other assorted data
│   |   ├── task1.txt       # task1 solution file
|   |   └── task2.txt       # task2 solution file
|   |
│   ├── task1.py            # Generate task1 model
│   └── task2.py            # Generate task2 model
|
├── classes                 # Classes to store branch, bus, and generator data
│   ├── branch.py           # Branch class
│   ├── bus.py              # Bus class
│   └── generator.py        # Generator class
|
|── data                    # Data files
|   ├── branches.csv        # Branches dataset
│   ├── buses.csv           # Buses dataset
│   ├── generators.csv      # Generators dataset
|   └── scaledcov.txt       # Scaled covariance matrix for task 2
|
|── cost_distribution.py    # Generate cost distribution plot and calculate VaR
|
└── main.py                 # Generate solution file for given task. Also contains some task 3 logic
```