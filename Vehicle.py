import helpers


class Vehicle:
    stages: list = None


class Stage:
    def __init__(self, name="", massTotal=None, massFuel=None, massDry=None, gLim=None, minThrottle=None, throttle=None,
                 shutdownRequired=None, engines=None, staging=None):
        if staging is None:
            staging = {}
        if engines is None:
            engines = []
        self.name = name
        self.massTotal: float = massTotal
        self.massFuel: float = massFuel
        self.massDry: float = massDry
        self.gLim: float = gLim
        self.minThrottle: float = minThrottle
        self.throttle: float = throttle
        self.shutdownRequired: bool = shutdownRequired
        self.engines: list = engines
        self.staging: dict = staging
        self.mode = 0
        self.maxT = 0

    def get_thrust(self):
        f = 0
        dm = 0

        for engine in self.engines:
            isp = engine.isp
            dm_ = engine.flow
            dm += dm_
            f += isp * dm_ * helpers.g0

        isp = f / (dm * helpers.g0)
        return f, dm, isp


class State:
    time = None
    mass = None
    radius = None
    velocity = None
    cser = None
    rbias = None
    rd = None
    rgrav = None
    vgo = None
    tb = None
    tgo = None

    def __init__(self, time, mass, radius, velocity, cser, rbias, rd, rgrav, vgo, tb, tgo):
        self.time = time
        self.mass = mass
        self.radius = radius
        self.velocity = velocity
        self.cser = cser
        self.rbias = rbias
        self.rd = rd
        self.rgrav = rgrav
        self.vgo = vgo
        self.tb = tb
        self.tgo = tgo