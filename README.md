# optimization_project_ieor4004
Final project for IEOR 4004 - Introduction to Optimization @ Columbia Engineering.

"The Optimizers" Roster:
- Alina Rodriguez
- Xueying Hu
- Sitong Zhong
- Daniel Rozenzaft
- Mars Dai

To run:
- `python main.py [task]`

This will generate a solution file at `tasks/solutions/[task].txt`.

Language:
- Python 3.9.9

Dependencies:
- gurobipy package installation
- Gurobi license

Contents:
```
┌── README.md               # This document!
|
├── tasks                   # Task models
│   ├── task1.py            # Generate task1 model (in testing as of this commit)
│   └── task2.py            # Generate task2 model (in development as of this commit)
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
└── main.py                 # Generate solution file for given task
```