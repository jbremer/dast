
class Container:
    def __init__(self, *args, **kwargs):
        self._order = []
        self._items = []

        # add the items, if they're given in the constructor
        for key, value in kwargs.items():
            self._items.append(key)
            setattr(self, key, value)

    def add_item(self, key, value):
        self._items.append(key)
        self._order.append(key)
        setattr(self, key, value)

    def items(self):
        return dict((key, getattr(self, key)) for key in self._items)

    def __repr__(self):
        items = self._order + [x for x in self._items if x not in self._order]
        return 'Container(%s)' % ', '.join(
            '%s=%s' % (key, getattr(self, key)) for key in items)

    def __cmp__(self, other):
        if not isinstance(other, Container):
            return other.__cmp__(self)
        return self.items() != other.items()

class Struct:
    def __init__(self, name, *args):
        self.name = name
        self.items = args

    def parse(self, data, offset=0):
        ret = Container()
        ret._ = getattr(self, '_', None)
        for item in self.items:
            item._ = ret
            value = item.parse(data, offset)
            offset += item.sizeof()
            ret.add_item(item.name, value)
        return ret

    def build(self, value):
        ret = ''
        for item in self.items:
            ret += item.build(getattr(value, item.name))
        return ret

    def sizeof(self):
        return sum(item.sizeof() for item in self.items)
