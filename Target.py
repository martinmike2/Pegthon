class Target:
    angle = None
    normal = None
    radius = None
    velocity = None
    rdval = None

    def __init__(self, angle, normal, radius, velocity, rdval):
        self.angle = angle
        self.normal = normal
        self.radius = radius
        self.velocity = velocity
