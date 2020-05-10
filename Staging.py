class Staging:
    def __init__(self, jettison=False, waitbeforeJettison=None, ignition=False, waitBeforeIgnition=None, ullage="", ullageBurnDuration=0, postUllageBurn=0):
        self.jettison = jettison
        self.waitBeforeJettison = waitbeforeJettison
        self.ignition = ignition
        self.waitBeforeIgnition = waitBeforeIgnition
        self.ullage = ullage
        self.ullageBurnDuration = ullageBurnDuration
        self.postUllageBurn = postUllageBurn

    def to_dict(self):
        return {
            "jettison": self.jettison,
            "waitBeforeJettison": self.waitBeforeJettison,
            "ignition": self.ignition,
            "waitBeforeIgnition": self.waitBeforeIgnition,
            "ullage": self.ullage,
            "ullageBurnDuration": self.ullageBurnDuration,
            "postUllageBurn": self.postUllageBurn
        }