from mock import Mock, RunTests, TestCase

from svgbatch.path import Path, PathData, ParseError


class PathDataTest(TestCase):

    def test_to_tuples_typical(self):
        data = [
            ' M 1, 2 L 3.0, 4.0 L 5, 6.0 Z ',
            'M 1, 2 L 3.0, 4.0 L 5, 6.0 Z',
            'M 1,2 L 3.0,4.0 L 5,6.0 Z',
            'M 1 2 L 3.0 4.0 L 5 6.0 Z',
            'M1, 2 L3.0, 4.0 L5, 6.0 Z',
            'M1,2 L3.0,4.0 L5,6.0 Z',
            'M1 2 L3.0 4.0 L5 6.0 Z',
            'M 1, 2L 3.0, 4.0L 5, 6.0Z',
            'M 1,2L 3.0,4.0L 5,6.0Z',
            'M 1 2L 3.0 4.0L 5 6.0Z',
            'M1, 2L3.0, 4.0L5, 6.0Z',
            'M1,2L3.0,4.0L5,6.0Z',
            'M1 2L3.0 4.0L5 6.0Z',
        ]
        expected = [ ('M', 1, 2), ('L', 3.0, 4.0), ('L', 5, 6.0), ('Z',)]
        for input in data:
            pathData = PathData(input)
            actual = pathData.to_tuples()
            self.assertEquals(actual, expected, 'for %s' % (input,))


    def test_to_tuples_thorough(self):
        data = [
            ('',            []),
            (' ',           []),
            ('a',           [('a',)]),
            (' a ',         [('a',)]),
            ('a1',          [('a', 1)]),
            ('a-1',         [('a', -1)]),
            (' a 1 ',       [('a', 1)]),
            (' a -1 ',      [('a', -1)]),
            ('a1.0',        [('a', 1.0)]),
            (' a 1.0 ',     [('a', 1.0)]),
            (' a -1.0 ',    [('a', -1.0)]),
            ('ab',          [('a',), ('b',)]),
            ('a b',         [('a',), ('b',)]),
            (' a b ',       [('a',), ('b',)]),
            ('a1b',         [('a', 1), ('b',)]),
            ('a-1b',        [('a', -1), ('b',)]),
            (' a 1 b ',     [('a', 1), ('b',)]),
            (' a -1 b ',    [('a', -1), ('b',)]),
            ('a1.0b',       [('a', 1.0), ('b',)]),
            ('a-1.0b',      [('a', -1.0), ('b',)]),
            (' a 1.0 b ',   [('a', 1.0), ('b',)]),
            (' a -1.0 b ',  [('a', -1.0), ('b',)]),
            ('ab2',         [('a',), ('b', 2)]),
            ('ab-2',        [('a',), ('b', -2)]),
            ('a b2',        [('a',), ('b', 2)]),
            ('a b-2',       [('a',), ('b', -2)]),
            ('a b 2',       [('a',), ('b', 2)]),
            (' a b 2 ',     [('a',), ('b', 2)]),
            ('ab2.0',       [('a',), ('b', 2.0)]),
            ('ab-2.0',      [('a',), ('b', -2.0)]),
            ('a b2.0',      [('a',), ('b', 2.0)]),
            ('a b 2.0',     [('a',), ('b', 2.0)]),
            ('a b -2.0',    [('a',), ('b', -2.0)]),
            (' a b 2.0 ',   [('a',), ('b', 2.0)]),
            ('a1b2',        [('a', 1), ('b', 2)]),
            ('a-1b-2',      [('a', -1), ('b', -2)]),
            ('a1 b2',       [('a', 1), ('b', 2)]),
            ('a-1 b-2',     [('a', -1), ('b', -2)]),
            (' a 1 b 2 ',   [('a', 1), ('b', 2)]),
            ('a1.0b2.0',    [('a', 1.0), ('b', 2.0)]),
            ('a-1.0b-2.0',  [('a', -1.0), ('b', -2.0)]),
            ('a1.0 b2.0',   [('a', 1.0), ('b', 2.0)]),
            (' a 1.0 b 2.0 ',   [('a', 1.0), ('b', 2.0)]),
            (' a -1.0 b -2.0 ',   [('a', -1.0), ('b', -2.0)]),
            ('a1,2',        [('a', 1, 2),]),
            ('a1,-2',       [('a', 1, -2),]),
            ('a1 2',        [('a', 1, 2),]),
            ('a1 -2',       [('a', 1, -2), ]),
            (' a 1, 2 ',    [('a', 1, 2), ]),
            (' a 1, -2 ',   [('a', 1, -2), ]),
            (' a 1,2 ',     [('a', 1, 2), ]),
            (' a 1,-2 ',    [('a', 1, -2), ]),
            (' a 1 2 ',     [('a', 1, 2), ]),
            (' a 1 -2 ',    [('a', 1, -2), ]),
            ('a1 2',        [('a', 1, 2), ]),
            ('a1 2.0',      [('a', 1, 2.0), ]),
            ('a1,2b',       [('a', 1, 2), ('b',)]),
            ('a-1,-2b',     [('a', -1, -2), ('b',)]),
            ('a1 2b',       [('a', 1, 2), ('b',)]),
            ('a-1 -2b',     [('a', -1, -2), ('b',)]),
            ('aaaaa',       [('a', ), ('a', ), ('a', ), ('a', ), ('a', ),]),
            ('abcde',       [('a', ), ('b', ), ('c', ), ('d', ), ('e', ),]),
            ('a a a a a',   [('a', ), ('a', ), ('a', ), ('a', ), ('a', ),]),
            ('a b c d e',   [('a', ), ('b', ), ('c', ), ('d', ), ('e', ),]),
            ('a1,2,3,4,5',  [('a', 1, 2, 3, 4, 5)]),
            ('a1 2 3 4 5',  [('a', 1, 2, 3, 4, 5)]),
        ]
        for input, expected in data:
            pathData = PathData(input)
            actual = pathData.to_tuples()
            self.assertEquals(actual, expected, 'for %r' % (input,))

            # test types of int/floats too. assertEquals doesn't
            for actual_cmd, exp_cmd in zip(actual, expected):
                for actual_param, exp_param in zip(actual_cmd, exp_cmd):
                    self.assertEquals(
                        type(actual_param),
                        type(exp_param),
                        'for %s' % (input,))


    def test_to_tuples_bad(self):
        data = [
            ('0', "missing command at 0 in '0'"),
            (' 0', "missing command at 1 in ' 0'"),
            ('-', "missing command at 0 in '-'"),
            ('.', "missing command at 0 in '.'"),
            (',', "invalid comma at 0 in ','"),
            (' ,', "invalid comma at 1 in ' ,'"),
            ('M,', "invalid comma at 1 in 'M,'"),
        ]
        for input, message in data:
            pathData = PathData(input)
            self.assertRaisesWithMessage(ParseError, message,
                pathData.to_tuples)


    def test_to_loops_bad_command(self):
        path = PathData(('X',))
        self.assertRaisesWithMessage(
            ParseError,
            'unsupported svg path command: X',
            path.parse
        )


    def test_parse_incomplete_path(self):
        path = PathData(None)
        self.assertRaisesWithMessage(
            ParseError,
            'loop needs 3 or more verts',
            path.to_loops, [('M', 1, 2), ('Z')],
        )
        self.assertRaisesWithMessage(
            ParseError,
            'loop needs 3 or more verts',
            path.to_loops, [('M', 1, 2), ('L', 3, 4), ('Z')]
        )
        # has only 2 unique verts
        self.assertRaisesWithMessage(
            ParseError,
            'loop needs 3 or more verts',
            path.to_loops, [('M', 1, 2), ('L', 3, 4), ('L', 1, 2), ('Z')],
        )

    def test_to_loops_duplicated_final_point_stripped(self):
        path = PathData(None)
        actual = path.to_loops(
            [('M', 1, 2), ('L', 3, 4), ('L', 5, 6), ('L', 1, 2), ('Z')])
        expected = [ [(1, -2), (3, -4), (5, -6)], ]
        self.assertEquals(actual, expected)


    def test_parse_not_z_terminated(self):
        self.fail()

    def test_parse_relative(self):
        self.fail()

    def test_parse_horizontal(self):
        self.fail()

    def test_parse_vertical(self):
        self.fail()

    def test_parse_repeated_implicit_commands(self):
        self.fail()


if __name__=='__main__':
    RunTests(PathDataTest)

