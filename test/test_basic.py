import unittest


class MyTestCase(unittest.TestCase):


    def test_table(self):

        from rowpipe.codegen import make_row_processors
        from rowpipe.table import Table

        t = Table('foobar')
        t.add_column('i1',datatype='int')
        t.add_column('i2', valuetype='int')
        t.add_column('i3', valuetype='measure/int')
        t.add_column('f1',datatype='float')
        t.add_column('f2', valuetype='float')
        t.add_column('f3', valuetype='measure/float')

        for c in t:
            print c

    def test_transform(self):

        from rowpipe.codegen import make_row_processors
        from rowpipe.table import Table

        t = Table('foobar')
        t.add_column('i1', datatype='int', transform='^row_number')
        t.add_column('f1', datatype='float', transform='^row.float1')

        source_headers = 'i1 float1'.split()

        code = make_row_processors(source_headers, t)

        print code


if __name__ == '__main__':
    unittest.main()
