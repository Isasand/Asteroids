# -*- coding: utf-8 -*-
"""
Gruppuppgift: Asteroids - Objektorienterad Programmering
Nackademin IOT 17

Medverkande:
Isa Sand
Felix Edenborgh
Christopher Bryant

Stomme källkod:
Mark Dixon
"""

import math, copy
import pygame

from shape import Shape
from point import Point


class Polygon(Shape):
    def __init__(self, points=[], x=0, y=0, rotation=0):
        """ points = all coordinates for the lines in the polygon
            x, y   = the 2-dimensional coordinates for the location of the polygon
            rotation = how many degrees the polygon should be rotated
            """
        super().__init__( x, y, rotation )
        # Make our own copy of all the points that make up this polygon
        self.points = list(points)


    def draw(self, screen):
        # Since polygons can be rotated, we need to "translate" all the points
        # by the amount of rotation before we draw them:
        points = self.getRotatedPoints()
        # Convert our point objects into a list of tuples that PyGame expects:
        vectors=[]
        for p in points:
            vectors.append( (p.x, p.y) )
        pygame.draw.polygon( screen,  (255,255,255), vectors, 1 )


    def getRotatedPoints(self):
        """
        getRotatedPoints() takes all points in self.points and transforms them
        mathematically by a given rotation angle (self.rotation)
        :return: returns a new list of points that are rotated
        """
        rotated_points=copy.deepcopy(self.points)
        center = self.findCenter()
        for i in range(len(rotated_points)):
            p = rotated_points[i]
            x = ( (p.x-center.x) * math.cos( math.radians(self.rotation)) ) \
                - ( (p.y-center.y) * math.sin( math.radians(self.rotation)) ) \
                + center.x/2.0 + self.position.x
            y = ( (p.x-center.x) * math.sin( math.radians(self.rotation))) \
                + ((p.y-center.y) * math.cos( math.radians(self.rotation))) \
                + center.y/2.0 + self.position.y
            rotated_points[i].x = x
            rotated_points[i].y = y
        return rotated_points


    def findArea(self):
        """
        Compute the area of the polygon using some fun mathematics.
        This could be useful for advanced colission detection.
        :return: estimate of the area of the polygon
        """
        sum = 0
        i = 0
        j = 1
        while i < len(self.points):
            sum += (self.points[i].x * self.points[j].y) - (self.points[j].x * self.points[i].y )
            i+=1
            j=(j+1)%len(self.points)

        return math.fabs( sum/2 )


    def findCenter(self):
        """
        Computes the center point of the polygon - helps us rotate polygons more nicely
        Just ignore the maths :)
        :return: a Point (x,y) representing the "center of gravity" of the polygon
        """
        sum = Point(0,0)
        i = 0
        j = 1
        while i < len(self.points):
            sum.x +=  (self.points[i].x + self.points[j].x ) \
                        * ( self.points[i].x * self.points[j].y - self.points[j].x * self.points[i].y )
            sum.y +=  (self.points[i].y + self.points[j].y ) \
                        * ( self.points[i].x * self.points[j].y - self.points[j].x * self.points[i].y )
            i+=1
            j=(j+1)%len(self.points)
        area = self.findArea()
        return Point( math.fabs( sum.x/(6*area)), math.fabs( sum.y/(6*area)) )


    def contains(self, point):
        """
        contains()  - used for collission detection. Computes if a given Point is inside
        or outside of the polygon.
        :param point: Which point
        :return: True or False depending on if the point is inside or not
        """
        crossingNumber = 0.0
        i = 0
        j = 1
        points = self.getRotatedPoints()
        while i < len(points):
            if ( ( ( ( points[i].x < point.x ) and ( point.x <= points[j].x ) ) or
                   ( ( points[j].x < point.x ) and ( point.x <= points[i].x ) ) ) and
                 ( point.y > points[i].y + ( points[j].y - points[i].y ) / ( points[j].x - points[i].x ) * ( point.x - points[i].x ) )
               ):
                crossingNumber+=1
            i+=1
            j=(j+1)%len(self.points)

        return crossingNumber % 2 == 1


    def collide(self, poly):
        """
        We override collide() to test if two polygons overlapp each other or not
        This can be used to test e.g. if an astroid and a ship have collided
        Or if two asteroids have collided.
        :param poly: Another object of typ Polygon
        :return: True or False depending on if the two objects intersect or not.
        """
        points = poly.getRotatedPoints()

        for p in points:
            if self.contains( p ):
                return True

        return False
