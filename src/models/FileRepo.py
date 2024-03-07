from collections import namedtuple

PointBase = namedtuple('PointBase', ['x', 'y'])

class Point(PointBase):
    def getX(self):
        return self.x
    def getY(self):
        return self.y