Row Data Pipeline
=================

The Rowpipe library manages row-oriented data transformers. Clients can create a RowProcessor() that has schema, composed of tables and columns, where each column cna have a "transform" that describes how to alter the data in the column.

.. code-block:: python

    from rowpipe.table import Table
    from rowpipe.processor import RowProcessor

    def doubleit(v):
        return int(v) * 2

    env = {
        'doubleit': doubleit
    }

    t = Table('foobar')
    t.add_column('id', datatype='int')
    t.add_column('other_id', datatype='int', transform='^row.a')
    t.add_column('i1', datatype='int', transform='^row.a;doubleit')
    t.add_column('f1', datatype='float', transform='^row.b;doubleit')
    t.add_column('i2', datatype='int', transform='^row.a')
    t.add_column('f2', datatype='float', transform='^row.b')


In this table definition, ``other_id`` and ``i2`` columns are  initialized to the valu of the ``a`` column in the input row,
The  ``i1`` column is initialized to the input row ``a`` column, then the ``doubleit`` function is called on the value. In the last step, all of the values are cast to the types specified in the ``datatype`` column.

The RowProcessor is then run using this table definition, and an input generator:

.. code-block:: python

    class Source(object):

        headers = 'a b'.split()

        def __iter__(self):
            for i in range(N):
                yield i, 2*i

    rp = RowProcessor(Source(), t, env=env)



Then, ``rp`` is a generator that returns ``RowProxy`` objects, which can be indexed as integers or by clolumn number:


.. code-block:: python

    for row in rp:
        v1 = row['f1']
        v2 = row[3]

The RowProcessor creates Python code files and executes them.

Transforms can have several steps, seperated by ';'. The first, prefixes with a '^', initializes the value for the rest of the transforms. A transform that is prefixes with a '!' is executed on exceptions.  Transform functions can have a variable signature; the tranform processor matches argument names. Valid argument names are:

- row. A rowProxy object for the input row. Allows access to any input row value
- row_n. Row number.
- scratch. A dict for temporary storage
- errors. A defaultdict(set) for storing error reports for columns. Keys are column names
- accumulator. A dict for accumulating value, such as sums.
- pipe. Unused
- bundle. Unused
- source. Reference to the input generator that is generating rows
- v . The input row value
- header_s. The header for the column in the input row.
- i_s. The index of the column in the input row
- header_d. The header for the column in the output row.
- i_d.  The index of the column in the output row

Notes
-----

This repo still contains old code for Row Pipelines, which are in the ``pipeline.py`` file. These components can be combined to performd defined operations on rows, such as skipping rows based on a predicate, altering the number of rows, returning on ly the head or tail, etc. The code is not currently used ot tested.



