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

        true(ULInt16, 4, '\x01\x02\x03\x04\x05\x06\x07\x08',
            [0x201, 0x403, 0x605, 0x807])
        true(UBInt16, 4, '\x01\x02\x03\x04\x05\x06\x07\x08',
            [0x102, 0x304, 0x506, 0x708])
        true(SLInt32, 2, '\x00\x00\x00\x00\x01\x00\x00\x00', [0, 1])
        true(SBInt64, 2, '\xff' * 15 + '\x00', [-1, -256])

if __name__ == '__main__':
    unittest.main()
