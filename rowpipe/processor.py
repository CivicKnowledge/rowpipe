# Copyright (c) 2016 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE.txt

"""

Row generating row processor

"""

from rowgenerators import Source
from rowpipe.codegen import make_row_processors, exec_context

class RowProcessor(Source):
    """
    """

    def __init__(self, source, dest_table, env=None):

        super(RowProcessor, self).__init__(None)

        self.source = source
        self.dest_table = dest_table

        self.env = exec_context()

        if env is not None:
            self.env.update(env)

        self.env['bundle'] = None
        self.env['source'] = self.source
        self.env['pipe'] = None

        self.scratch = {}
        self.accumulator = {}
        self.errors = {}

        self.code = make_row_processors(source.headers, dest_table, env=env)

        self.code_path = self.write_code()

        exec (compile(self.code, self.code_path, 'exec'), self.env)

        self.procs = self.env['row_processors']

    def write_code(self):
        import hashlib
        import os

        path = '/tmp/rowprocessor/{}.py'.format(hashlib.md5(self.code).hexdigest())

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path,'w') as f:
            f.write(self.code)

        return path

    @property
    def headers(self):
        """Return a list of the names of the columns of this file, or None if the header is not defined.

        This should *only* return headers if the headers are unambiguous, such as for database tables,
        or shapefiles. For other files, like CSV and Excel, the header row can not be determined without analysis
        or specification."""

        return None

    @headers.setter
    def headers(self, v):
        raise NotImplementedError

    @property
    def meta(self):
        return {}

    def __iter__(self):
        """Iterate over all of the lines in the file"""
        from rowgenerators import RowProxy
        self.start()

        bundle = self.env['bundle']
        pipe = self.env['pipe']

        rp1 = RowProxy(self.source.headers) # The first processor step uses the source row structure
        rp2 = RowProxy(self.dest_table.headers) # Subsequent steps use the dest table

        for i, row in enumerate(self.source):

            if self.limit and i > self.limit:
                break

            try:
                rp = rp1
                for proc in self.procs:
                    row = proc(rp.set_row(row), i, self.errors, self.scratch, self.accumulator,
                               pipe, bundle, self.source)

                    # After the first round, the row has the destination headers.
                    rp = rp2

                yield row
            except Exception as e:
                raise

        self.finish()




    def _get_row_gen(self):
        """ Returns generator over all rows of the source. """
        raise NotImplementedError('Subclasses of SourceFile must provide a _get_row_gen() method')

    def start(self):
        pass

    def finish(self):
        pass