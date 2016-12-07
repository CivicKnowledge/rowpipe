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

        from rowpipe.table import Table
        from rowpipe.processor import RowProcessor
        from contexttimer import Timer
        def doubleit(v):
            return int(v) * 2

        env = {
            'doubleit': doubleit
        }

        t = Table('foobar')
        t.add_column('id', datatype='int')
        t.add_column('other_id', datatype='int', transform='^row.i1')
        t.add_column('i1', datatype='int', transform='doubleit')
        t.add_column('f1', datatype='float', transform='doubleit')
        t.add_column('i2', datatype='int', transform=';row.i1')
        t.add_column('f2', datatype='float', transform=';row.f1')

        N = 100000

        class Source(object):

            headers = 'i1 f1'.split()

            def __iter__(self):
                for i in range(N):
                    yield i, 2*i

        rp = RowProcessor(Source(), t, env)

        count = 0
        sum = 0
        with Timer() as t:
            for row in rp:
                count += 1
                sum += row[0]

        print 'Rate=', float(N) / t.elapsed 

if __name__ == '__main__':
    unittest.main()
