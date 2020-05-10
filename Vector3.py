import math


class Vector3(tuple):
    x: float = None
    y: float = None
    z: float = None

    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def magnitude(self):
        return float(math.sqrt(self.x**2 + self.y**2 + self.z**2))

    def add(self, other):
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def sub(self, other):
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def normalized(self):
        mag: float = self.magnitude()
        return Vector3(
            self.x / mag,
            self.y / mag,
            self.z / mag
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def ang(self, other):
        return math.acos(
            self.dot(other) / self.magnitude() * other.magnitude()
        )

    def project(self, other):
        top = self.dot(other)
        bot = other.dot(other)
        return (top / bot) * other