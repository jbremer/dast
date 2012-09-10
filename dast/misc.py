
def sizeof(obj):
    return obj.sizeof()

class Value:
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def parse(self, data, offset=0):
        return self.func(self._)

    def build(self, value):
        return ''

    def sizeof(self):
        return 0
