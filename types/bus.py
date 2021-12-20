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

    def __str__(self):
        """Printed representation of a bus."""
        return str(dict(zip(self._KEYS, self._VALUES)))

    def __repr__(self):
        """Object representation of bus."""
        return repr(dict(zip(self._KEYS, self._VALUES)))


def load_buses(dataset):
    """Static method: load bus.csv dataset and create a list of bus."""
    buses = []
    for row in csv.DictReader(open(dataset), fieldnames=_KEYS):
        if row['bus'].isdigit():  # don't add top or bottom row as a bus object
            buses.append(Bus(**row))
    return buses
