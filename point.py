
import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def getX( self ):
        return self.x
    def getY( self ):
        return self.y

    def __add__(self, b):
        return Point( self.x + b.x, self.y + b.y )

    def __sub__(self, b):
        return Point( self.x - b.x, self.y - b.y )

    def distanceFromOrigin(self):
        return math.sqrt( self.x**2 + self.y**2 )


