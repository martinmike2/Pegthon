class Engine:
    def __init__(self, isp=0, thrust=0, flow=0):
        self.isp = isp
        self.thrust = thrust
        self.flow = flow

    def to_tuple(self):
        return self.isp, self.thrust, self.flow
