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
    """Load branch.csv dataset and return a list of branches."""
    with open(dataset) as data:
        branches = csv.DictReader(data)
        return [Branch(**row) for row in branches if row['branch'].isdigit()]
