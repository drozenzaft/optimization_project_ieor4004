"""Branch class and loader."""
import csv


class Branch():

    def __init__(self, **kwargs):
        """Branch constructor."""
        self.branch = int(kwargs['branch'])
        self.from_bus = int(kwargs['from'])
        self.to_bus = int(kwargs['to'])
        self.x = float(kwargs['x'])
        self.u = float(kwargs['u'])

        self._KEYS = ('branch', 'from', 'to', 'x', 'u')
        self._VALUES = (self.branch, self.from_bus, self.to_bus, self.x, self.u)

    def __str__(self):
        """Printed representation of a branch."""
        return str(dict(zip(self._KEYS, self._VALUES)))

    def __repr__(self):
        """Object representation of branch."""
        return repr(dict(zip(self._KEYS, self._VALUES)))


def load_branches(dataset):
    """Static method: load branch.csv dataset and create a list of branch."""
    branches = []
    for row in csv.DictReader(open(dataset)):
        if row['branch'].isdigit():  # don't add bottom row as a branch object
            branches.append(Branch(**row))
    return branches
