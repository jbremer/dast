
class Array:
    def __init__(self, item, min_=None, max_=None):
        self.item = item
        self.min_ = min_
        self.max_ = max_

        # minimum size
        self.size = min_ * item.sizeof()

    def parse(self, data, offset=0):
        ret = []
        for x in xrange(self.min_):
            ret.append(self.item.parse(data, offset))
            offset += self.item.sizeof()

        x += 1

        if self.max_ and self.max_ > self.min_:
            while x < self.max_ and len(data) - offset >= self.item.sizeof():
                ret.append(self.item.parse(data, offset))
                offset += self.item.sizeof()
                x += 1

        self.size = x * self.item.sizeof()
        return ret

    def build(self, data):
        ret = ''
        for x in xrange(len(data)):
            ret += self.item.build(data[x])
        return ret

    def sizeof(self):
        return self.size
