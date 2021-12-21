"""Bus class and loader."""
import csv

_KEYS = ('bus', 'load')


class Bus():

    def __init__(self, **kwargs):
        """Bus constructor."""
        self.bus = int(kwargs['bus'])
        self.load = float(kwargs['load'])

        self._KEYS = _KEYS
        self._VALUES = (self.bus, self.load)

    def generators(self, generators):
        """Get generators located in this bus."""
        return [generator for generator in generators if generator.bus == self.bus]

    def branches(self, branches):
        """Get associated branches in 2-value tuple (from, to)."""
        from_branches, to_branches = [], []
        [
            from_branches.append(branch) if branch.from_bus == self.bus else
            to_branches.append(branch) if branch.to_bus == self.bus
            else None for branch in branches
        ]
        return (from_branches, to_branches)

    def __str__(self):
        """Printed representation of a bus."""
        return str(dict(zip(self._KEYS, self._VALUES)))

    def __repr__(self):
        """Object representation of bus."""
        return repr(dict(zip(self._KEYS, self._VALUES)))


def load_buses(dataset):
    """Load bus.csv dataset and return a list of buses."""
    with open(dataset) as data:
        buses = csv.DictReader(data, fieldnames=_KEYS)
        return [Bus(**row) for row in buses if row['bus'].isdigit()]
