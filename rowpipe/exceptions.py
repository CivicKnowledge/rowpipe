# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE.txt

"""Pipes, pipe segments and piplines, for flowing data from sources to partitions.

"""

from valuetype.exceptions import TooManyCastingErrors

class RowPipeError(Exception):
    pass

class ConfigurationError(RowPipeError):
    pass

