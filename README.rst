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


    for row in rp:
        v1 = row['f1']
        v2 = row[3]

