from collections import namedtuple

PointBase = namedtuple('PointBase', ['x', 'y', 'time'])

class Point(PointBase):
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getTime(self):
        return self.time