import helpers


class Stage:
    def __init__(self, name="", massTotal=None, massFuel=None, massDry=None, gLim=None, minThrottle=None, throttle=None,
                 shutdownRequired=None, engines=[], staging={}):
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
