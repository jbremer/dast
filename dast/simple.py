import struct

class _SimpleType:
    def __init__(self, name, fmt, size):
        self.name = name
        self.fmt = fmt
        self.size = size

    def parse(self, data, offset=0):
        return struct.unpack_from(self.fmt, data, offset)[0]

    def build(self, value):
        return struct.pack(self.fmt, value)

    def sizeof(self):
        return self.size

def SBInt8(name): return _SimpleType(name, 'b', 1)
def UBInt8(name): return _SimpleType(name, 'B', 1)
def SLInt8(name): return _SimpleType(name, 'b', 1)
def ULInt8(name): return _SimpleType(name, 'B', 1)

def SBInt16(name): return _SimpleType(name, '>h', 2)
def UBInt16(name): return _SimpleType(name, '>H', 2)
def SLInt16(name): return _SimpleType(name, '<h', 2)
def ULInt16(name): return _SimpleType(name, '<H', 2)

def SBInt32(name): return _SimpleType(name, '>i', 4)
def UBInt32(name): return _SimpleType(name, '>I', 4)
def SLInt32(name): return _SimpleType(name, '<i', 4)
def ULInt32(name): return _SimpleType(name, '<I', 4)

def SBInt64(name): return _SimpleType(name, '>q', 8)
def UBInt64(name): return _SimpleType(name, '>Q', 8)
def SLInt64(name): return _SimpleType(name, '<q', 8)
def ULInt64(name): return _SimpleType(name, '<Q', 8)

def BFloat32(name): return _SimpleType(name, '>f', 4)
def LFloat32(name): return _SimpleType(name, '<f', 4)

def BFloat64(name): return _SimpleType(name, '>F', 8)
def LFloat64(name): return _SimpleType(name, '<F', 8)
