from vectors2d import Vector
import matplotlib.pyplot as plt
import math


class Obstacle:
    """The base class for all obstacles. Obstacles can be seen by actors."""

    def __init__(self, position):
        self.pos = Vector(position[0], position[1])


class Circle(Obstacle):
    """A circular obstacle."""

    def __init__(self, position, radius):
        Obstacle.__init__(self, position)
        self.rad = radius
        self.rad_sq = radius**2


class Wall(Obstacle):
    """A straight wall"""

    def __init__(self, start, stop):
        self.start = Vector(start[0], start[1])
        self.stop = Vector(stop[0], stop[1])
        self.center = (self.start + self.stop) / 2
        self.vector = self.stop - self.start

        self.length = (self.stop - self.start).length()

        Obstacle.__init__(self, self.center)

    def determinant(self, point):
        return (self.stop.x - self.start.x) * (point.y - self.start.y) - (self.stop.y - self.start.y) * (point.x - self.start.x)

    def side(self, point):
        """Returns -1 if the point is on the left and +1 if it is on the right."""
        return math.copysign(1, - self.determinant(point))

    def orthonormal_vector_to(self, point):
        return self.side(point) * self.vector.orthonormal()

    def distance_to(self, point):
        """Calculates the distance of the wall to a point"""

        return abs(self.determinant(point) / self.length)

    def distance_sq_to(self, point):
        """Calculates the distance squared of the wall to a point"""

        return (self.determinant(point) / self.length)**2

    def intersects(self, point, vector):
        """Determines if a line given by a start point and a vector intersects the wall."""
        r = self.vector
        s = vector
        q = point
        p = self.start

        r_x_s = r.cross(s)

        if abs(r_x_s) >= 0.000001:  # if the cross product of the wall and the given vector is not zero
            t = (q - p).cross(s / r_x_s)
            u = (p - q).cross(r / (- r_x_s))
            if 0 <= t <= 1 and 0 <= u <= 1:
                return True

        return False

