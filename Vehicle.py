import helpers
from Engine import Engine


class Vehicle:
    stages: list = []
    sequence: list = []

    def add_sequence(self, sequence):
        self.sequence.append(sequence)

    def add_stage(self, stage):
        self.stages.append(
            Stage(
                name=stage["name"],
                massTotal=stage["mass_total"],
                massFuel=stage["mass_fuel"],
                massDry=stage["mass_dry"],
                gLim=stage["g_lim"],
                minThrottle=stage["minimum_throttle"],
                throttle=stage["throttle"],
                shutdownRequired=stage["shutdown_required"],
                staging=stage["staging"],
                engines=stage["engines"]
            )
        )

class Stage:
    engines = []
    staging = {}

    def __init__(self, name="", massTotal=None, massFuel=None, massDry=None, gLim=None, minThrottle=None,
                 throttle=None,
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
        self.staging: dict = staging
        self.mode = 0
        self.maxT = 0

        for engine in engines:
            self.add_engine(engine)

    def add_engine(self, engine):
        self.engines.append(Engine(engine["isp"], engine["thrust"], engine["flow"]))

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
