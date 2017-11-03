import math

import pygame

from point import Point
from shape import Shape


class Circle(Shape):
    """
    Circle extends the base class Shape to handle circles.
    A circle has a position, a radius, and an rotation (yes, really!)
    """
    def __init__(self, x, y, r, rotation ):
        super().__init__(  x, y, rotation )
        self.radius = int(r)
        self.linewidth = 1

    def draw(self, screen):
        super().draw(screen)
        pos = (int(self.position.x), int(self.position.y) )
        pygame.draw.circle( screen,  (255,255,255), pos, self.radius, self.linewidth )

    def contains(self, point):
        # Not used in basic game design - can you find a use for this?
        pointRelativeToCircle = point - self.position
        pointDistanceFromCircleOrigin = pointRelativeToCircle.distanceFromOrigin()
        return pointDistanceFromCircleOrigin <= self.radius