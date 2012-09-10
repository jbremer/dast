import unittest
from dast import *

class DastTests(unittest.TestCase):
    def test_simple_types(self):
        def true(typ, data, value):
            self.assertEqual(typ(None).parse(data), value)
            self.assertEqual(typ(None).build(value), data)
        def false(typ, data, value):
            self.assertNotEqual(typ(None).parse(data), value)

        true(SBInt8, '\x01', 1)
        true(SBInt8, '\x40', 0x40)
        true(SBInt8, '\xfe', -2)
        false(SBInt8, '\xfe', 254)

        true(ULInt8, '\x01', 1)
        true(ULInt8, '\x40', 0x40)
        false(ULInt8, '\xfe', -2)
        true(ULInt8, '\xfe', 254)

        true(SBInt16, '\x01\x02', 0x102)
        true(SBInt16, '\x40\x00', 0x4000)
        true(SBInt16, '\xfe\xff', -257)
        false(SBInt16, '\xfe\xff', 0xfeff)

        true(ULInt16, '\x01\x02', 0x201)
        true(ULInt16, '\x40\x00', 0x40)
        false(ULInt16, '\xfe\xff', -257)
        true(ULInt16, '\xfe\xff', 0xfffe)

        true(SBInt32, '\x01\x02\x03\x04', 0x01020304)
        true(SBInt32, '\xff\xff\xff\xff', -1)
        false(SBInt32, '\xfe\xff\xff\xff', -1)

        true(SLInt32, '\x01\x02\x03\x04', 0x04030201)
        true(SLInt32, '\xff\xff\xff\xff', -1)
        true(SLInt32, '\xfe\xff\xff\xff', -2)

        true(ULInt32, '\xfe\xff\xff\xff', 0xfffffffe)
        false(UBInt32, '\xfe\xff\xff\xff', 0xfffffffe)

        true(SLInt64, '\x01\x02\x03\x04\x05\x06\x07\x08', 0x0807060504030201)
        true(UBInt64, '\x01\x02\x03\x04\x05\x06\x07\x08', 0x0102030405060708)
        true(SLInt64, '\xf0\xff\xff\xff\xff\xff\xff\xff', -16)
        false(SBInt64, '\xf0\xff\xff\xff\xff\xff\xff\xff', -16)

    def test_array(self):
        def true(typ, count, data, value):
            self.assertEqual(Array(typ(None), count).parse(data), value)
            self.assertEqual(Array(typ(None), count).build(value), data)
        def size(typ, data, siz):
            typ.parse(data)
            self.assertEqual(typ.sizeof(), siz)
        eq = self.assertEqual

        true(ULInt16, 4, '\x01\x02\x03\x04\x05\x06\x07\x08',
            [0x201, 0x403, 0x605, 0x807])
        true(UBInt16, 4, '\x01\x02\x03\x04\x05\x06\x07\x08',
            [0x102, 0x304, 0x506, 0x708])
        true(SLInt32, 2, '\x00\x00\x00\x00\x01\x00\x00\x00', [0, 1])
        true(SBInt64, 2, '\xff' * 15 + '\x00', [-1, -256])

        eq(Array(SLInt16(None), 3, 7).parse('a' * 6), [0x6161] * 3)
        eq(Array(SLInt16(None), 3, 7).parse('a' * 10), [0x6161] * 5)
        eq(Array(SLInt16(None), 3, 7).parse('a' * 14), [0x6161] * 7)
        eq(Array(SLInt16(None), 3, 7).parse('a' * 16), [0x6161] * 7)
        size(Array(SLInt16(None), 3, 7), 'a' * 6, 6)
        size(Array(SLInt16(None), 3, 7), 'a' * 10, 10)
        size(Array(SLInt16(None), 3, 7), 'a' * 14, 14)

        # empty list
        eq(Array(SLInt8(None), 0).parse('aaaa'), [])

        # nested arrays
        self.assertEqual(Array(Array(UBInt8('a'), 4), 5).parse('a' * 20),
            [[0x61] * 4] * 5)

    def test_container(self):
        self.assertEqual(Container(a=1, b=2), Container(b=2, a=1))
        self.assertNotEqual(Container(a=2, b=3), Container(a=2, b=4))
        self.assertEqual(Container(a=1, b=3), Container(b=3, a=1))

    def test_struct(self):
        def true(typ, data, value):
            self.assertEqual(typ.parse(data), value)
            self.assertEqual(typ.build(value), data)

        true(Struct(None, UBInt16('a'), UBInt16('b')), '\xaa\xbb\xcc\xdd',
            Container(a=0xaabb, b=0xccdd))
        true(Struct(None, Struct('x', UBInt8('a'), UBInt8('b')),
            Struct('y', UBInt8('c'), UBInt8('d'))), 'abcd', Container(
            x=Container(a=0x61, b=0x62), y=Container(c=0x63, d=0x64)))
        self.assertEqual(
            Struct(None, UBInt16(None), ULInt32(None)).sizeof(), 6)

        # empty struct
        self.assertEqual(Struct(None).parse('aaaa'), Container())

        # nested structs
        true(Struct('a', Struct('b', Struct('c', UBInt8('d')))), 'a',
            Container(b=Container(c=Container(d=0x61))))

    def test_data(self):
        eq = self.assertEqual

        eq(Data(None, lambda ctx: 32).parse('a' * 40), 'a' * 32)
        eq(Struct(None, UBInt8('length'), Data('data', 'length')).parse(
            '\x10' + 'a' * 16), Container(length=16, data='a' * 16))

    def test_combo(self):
        def true(typ, data, value):
            self.assertEqual(typ.parse(data), value)
            self.assertEqual(typ.build(value), data)

        # array nested inside struct
        true(Struct(None, Array(UBInt8('a'), 2)), 'aa',
            Container(a=[0x61, 0x61]))

        # struct nested in array
        true(Array(Struct('s', UBInt8('a'), UBInt16('b')), 2), 'abcdef',
            [Container(a=0x61, b=0x6263), Container(a=0x64, b=0x6566)])

        # variable length array nested in struct
        true(Struct(None, UBInt8('length'), Array(UBInt16('data'), 'length')),
            '\x02\x00\x01\x00\x02', Container(length=2, data=[1, 2]))

        # variable length array nested inside a struct inside a struct
        # with the length obtained by using a string
        true(Struct(None, UBInt8('length'), Struct('a', Array(ULInt32('b'),
            '_.length'))),
            '\x03\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00',
            Container(length=3, a=Container(b=[1, 2, 3])))

        # same as above, but length is obtained using a lambda
        true(Struct(None, UBInt8('length'), Struct('a',
            Array(ULInt32('b'), lambda ctx: ctx._.length))),
            '\x03\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00',
            Container(length=3, a=Container(b=[1, 2, 3])))

        # use same struct twice
        a = Struct('a', UBInt32('b'))
        true(Struct(None, Struct('a', a), Struct('b', a)),
            'aaaabbbb', Container(a=Container(a=Container(b=0x61616161)),
            b=Container(a=Container(b=0x62626262))))

        # compute a value
        true(Struct(None, UBInt8('major_version'),
            UBInt8('minor_version'), Value('version', lambda ctx: '%d.%d' % (
            ctx.major_version, ctx.minor_version))), '\x0d\x25',
            Container(major_version=13, minor_version=37, version='13.37'))

if __name__ == '__main__':
    unittest.main()
