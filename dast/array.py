
class Array:
    def __init__(self, item, min_=None):
        self.item = item
        self.min_ = min_

    def parse(self, data, offset=0):
        ret = []
        for x in xrange(self.min_):
            ret.append(self.item.parse(data, offset))
            offset += self.item.sizeof()
        return ret

    def build(self, data):
        ret = ''
        for x in xrange(len(data)):
            ret += self.item.build(data[x])
        return ret
