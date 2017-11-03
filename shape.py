from abc import ABC, abstractmethod

import math

from point import Point

class Shape(ABC):
    def __init__( self, x=0, y=0, rotation=0 ):
        self.position = Point(x,y)
        self.rotation = rotation
        self.pull = Point(0,0)
        self.angular_velocity = 0.0

    @abstractmethod
    def draw(self, screen):
        pass

    def update(self, width, height):
        """
        Update the position and orientation of the shape
        :param width: screen width to confine the shape to
        :param height: screen height to confine the shape to
        :return: 
        """
        # Update the position and orientation of the shape
        #  position is modified by "pull" - how much it should move each frame
        #  rotation is modified by "angular_velocity" - how much it should rotate each frame
        self.position += self.pull
        self.rotation += self.angular_velocity
        # Use modulus to ensure that the object never vanishes from the screen
        #  Position is wrapped to always be between  (0,0)  and  (width,height)
        #  Rotation is wrapped to always be between 0 and 360 degrees
        self.position.x %= width
        self.position.y %= height
        self.rotation %= 360


    def accelerate(self, acceleration):
        """
        Cause the object to start moving by giving it a little push
        :param acceleration: ammount to accelerate the shape by,  if 0 then the shape is slowed down instead
        """
        #
        if acceleration==0:
            self.pull.x *=0.9
            self.pull.y *=0.9
        else:
            self.pull.x += (acceleration * math.cos(math.radians(self.rotation)))
            self.pull.y += (acceleration * math.sin(math.radians(self.rotation)))

    def rotate(self, degrees):
        """
        Rotation the shape by a specific amount
        :param degrees: angle in degrees for the shape to be rotated by
        """
        self.rotation = ( self.rotation + degrees ) % 360;

    @abstractmethod
    def contains(self, point):
        if point:
            return True
        """
        Abstract base class to perform collission detection - should return true if a point is inside
        the shape
        :param point: Point to test for collission
        :return: True or False
        """
        return False

