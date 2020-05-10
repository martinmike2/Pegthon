class Guidance:
    vector = None
    pitch = None
    yaw = None
    pitchdot = None
    yawdot = None
    tgo = None

    def __init__(self, vector, pitch, yaw, pitchdot, yawdot, tgo):
        self.vector = vector
        self.pitch = pitch
        self.yaw = yaw
        self.pitchdot = pitchdot
        self.yawdot = yawdot
        self.tgo = tgo