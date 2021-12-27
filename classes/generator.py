"""Generator class and loader."""
import csv


class Generator():

    def __init__(self, **kwargs):
        """Generator constructor."""
        self.generator = int(kwargs['generator'])
        self.bus = int(kwargs['bus'])
        self.fuel = kwargs['fuel']
        self.pmax = float(kwargs['pmax'])
        self.sigma = float(kwargs['sigma'])

        self._KEYS = ('generator', 'bus', 'fuel', 'nuclear', 'pmax', 'sigma')
        self._VALUES = (self.generator, self.bus, self.fuel, self.pmax, self.sigma)

    def __str__(self):
        """Printed representation of a generator."""
        return str(dict(zip(self._KEYS, self._VALUES)))

    def __repr__(self):
        """Object representation of generator."""
        return repr(dict(zip(self._KEYS, self._VALUES)))


def load_generators(dataset='data/generators.csv'):
    """Load generators.csv dataset and return a list of generators. Optional: filter wind fuel generators (default no)."""
    with open(dataset) as data:
        generators = csv.DictReader(data)
        return [Generator(**row) for row in generators if row['generator'].isdigit()]
