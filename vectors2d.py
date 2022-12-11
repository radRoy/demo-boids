import math


class Vector(tuple):
    """A 2D vector"""

    def __new__(cls, x, y):
        # Vectors inherit from the tuple.
        return tuple.__new__(Vector, (x, y))

    def __init__(self, x, y):
        self.x = float(x)  # x coordinate
        self.y = float(y)  # y coordinate

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            # Multiplication turns into dot product if the other object is also a Vector
            return self.dot(other)
        else:
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        if isinstance(other, Vector):
            # Multiplication turns into dot product if the other object is also a Vector
            return other.dot(self)
        else:
            return Vector(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __setitem__(self, key, value):
        if key == 0:
            return Vector(value, self.y)
        elif key == 1:
            return Vector(self.x, value)

    def __abs__(self):
        return self.length()

    def length_sq(self):
        """Returns the squared length (magnitude) of the vector."""
        return (self.x * self.x) + (self.y * self.y)

    def length(self):
        """Returns the length (magnitude) of the vector."""
        return math.sqrt(self.length_sq())

    def inverse(self):
        """Returns the inverse of the vector."""
        return Vector(1.0 / self.x, 1.0 / self.y)

    def normalize(self):
        """Returns the normalized vector such that it's length is 1 but direction stays the same."""
        length = self.length()
        if length == 0.0:
            return Vector(0, 0)
        return Vector(self.x / length, self.y / length)

    def dot(self, other):
        """Returns the dot product of the vector and a given second vector."""
        return self.x * other.x + self.y * other.y

    def direction_to(self, point):
        """Returns a normalized vector that points into the direction of a given point."""
        return (point - self).normalize()

    def distance_sq_to(self, point):
        """Returns the distance squared to a given point."""
        return abs(self.x - point.x) ** 2 + abs(self.y - point.y) ** 2

    def distance_to(self, point):
        """Returns the distance to a given point."""
        return math.sqrt(self.distance_sq_to(point))

    def angle_to(self, point):
        """Returns the smallest, unsigned angle to a given point."""
        dot_prod = self.normalize().dot(point.normalize())
        try:
            return math.acos(dot_prod)
        except ValueError:
            if dot_prod >= 1:
                return math.acos(1)
            if dot_prod <= -1:
                return math.acos(-1)

    def orthogonal(self):
        """Always returns the orthogonal vector pointing to the right of the original vector."""
        return Vector(self.y, -self.x)

    def orthonormal(self):
        """Always returns the orthonormal vector (with length 1) pointing to the right of the original vector."""
        return self.orthogonal().normalize()

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def determinant(self, start, point):
        stop = start + self
        return (stop.x - start.x) * (point.y - start.y) - (stop.y - start.y) * (point.x - start.x)

    def side(self, start, point):
        """Returns -1 if the point is on the left and +1 if it is on the right."""
        return math.copysign(1, - self.determinant(start, point))
