
def _obtain(self, value):
    if value is None:
        return None

    if isinstance(value, (int, long)):
        return int(value)

    if isinstance(value, str):
        obj = self._
        for part in value.split('.'):
            obj = getattr(obj, part)
        return obj

    if callable(value):
        return value(getattr(self, '_', None))

class Array:
    def __init__(self, item, min_=None, max_=None):
        self.item = item
        self.name = item.name
        self.min_ = min_
        self.max_ = max_

    def parse(self, data, offset=0):
        ret = []

        # obtain the length
        min_ = _obtain(self, self.min_)
        max_ = _obtain(self, self.max_)

        # if min_ is zero, then x is not initialized automatically
        x = 0
        for x in xrange(min_):
            ret.append(self.item.parse(data, offset))
            offset += self.item.sizeof()

        x += 1

        if max_ and max_ > min_:
            while x < max_ and len(data) - offset >= self.item.sizeof():
                self.item._ = getattr(self, '_', None)
                ret.append(self.item.parse(data, offset))
                offset += self.item.sizeof()
                x += 1

        self.size = x * self.item.sizeof()
        return ret

    def build(self, value):
        ret = ''
        for x in xrange(len(value)):
            ret += self.item.build(value[x])
        return ret

    def sizeof(self):
        return self.size

class Data:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def parse(self, data, offset=0):
        self.size = _obtain(self, self.size)
        return data[offset:offset+self.size]

    def build(self, value):
        return value

    def sizeof(self):
        return self.size
