# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE.txt

"""
Tables and columns

"""

from rowpipe.valuetype import resolve_value_type
from tabulate import tabulate

class Table(object):

    def __init__(self, name):
        self.name = name
        self.columns = []

    def add_column(self, name, datatype=None, valuetype=None, transform=None):
        self.columns.append(Column(name, datatype, valuetype, transform))

    @property
    def headers(self):
        return [c.name for c in self.columns]


    def __iter__(self):

        for c in self.columns:
            yield c

    def __str__(self):

        headers = 'name datatype valuetype transform'.split()
        rows = [(c.name, c.datatype.__name__, c.valuetype.__name__, c.transform) for c in self.columns]

        return ('Table: {}\n'.format(self.name)) + tabulate(rows, headers)


class Column(object):

    def __init__(self, name, datatype=None, valuetype=None, transform=None):

        self.name = name
        self.transform = transform

        if valuetype is not None and datatype is None:
            self.valuetype = resolve_value_type(valuetype)
        elif datatype is not None:
            self.valuetype = resolve_value_type(datatype)

        self.datatype = self.valuetype.python_type()

    @property
    def expanded_transform(self):
        """Expands the transform string into segments """

        segments = Column._expand_transform_to_segments(self.transform)

        vt = self.valuetype if self.valuetype else self.datatype

        if segments:

            segments[0]['datatype'] = vt

            for s in segments:
                s['column'] = self

        else:

            segments = [Column.make_xform_seg(datatype=vt, column=self)]

        # If we want to add the find datatype cast to a transform.
        # segments.append(self.make_xform_seg(transforms=["cast_"+self.datatype], column=self))

        return segments

    def __repr__(self):
        return "<Column {name} dt={datatype} vt={valuetype} {transform}>"\
                .format(name=self.name, datatype=self.datatype.__name__, valuetype=self.valuetype.__name__,
                        transform=self.transform)


    @property
    def dict(self):
        return dict(
            name=self.name,
            datatype=self.datatype,
            valuetype=self.valuetype,
            transform=self.transform

        )

    @staticmethod
    def make_xform_seg(init_=None, datatype=None, transforms=None, exception=None, column=None):
        return {
            'init': init_,
            'transforms': transforms if transforms else [],
            'exception': exception,
            'datatype': datatype,
            'column': column
        }

    @staticmethod
    def _expand_transform_to_segments(transform):
        from .exceptions import ConfigurationError

        if not bool(transform):
            return []

        transform = transform.rstrip('|')

        segments = []

        for i, seg_str in enumerate(transform.split(';')):  # ';' seperates pipe stages
            pipes = seg_str.split('|')  # eperates pipes in each stage.

            d = Column.make_xform_seg()

            for pipe in pipes:

                if not pipe.strip():
                    continue

                if pipe[0] == '^':  # First, the initializer
                    if d['init']:
                        raise ConfigurationError('Can only have one initializer in a pipeline segment')
                    if i != 0:
                        raise ConfigurationError('Can only have an initializer in the first pipeline segment')
                    d['init'] = pipe[1:]
                elif pipe[0] == '!':  # Exception Handler
                    if d['exception']:
                        raise ConfigurationError('Can only have one exception handler in a pipeline segment')
                    d['exception'] = pipe[1:]
                else:  # Assume before the datatype
                    d['transforms'].append(pipe)

            segments.append(d)

        return segments




