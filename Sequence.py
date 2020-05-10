class Sequence:
    def __init__(self):
        self.sequence = []

    def add_sequence(self, time=0, type="", message=None, throttle=None, massLost=None, angle=None):
        base = {
            "time": time,
            "type": type
        }

        if message is not None:
            base["message"] = message
        if type == "throttle":
            base["throttle"] = throttle
        if type == "jettison":
            base["massLost"] = massLost
        if type == "roll":
            base["angle"] = angle

        self.sequence.append(base)

    def add_stage(self, time, message):
        self.add_sequence(time, "stage", message)

    def add_jettison(self, time, message, massLost):
        self.add_sequence(time, "jettison", message, massLost=massLost)

    def add_throttle(self, time, message, throttle):
        self.add_sequence(time, "throttle", message, throttle)

    def add_roll(self, time, message, angle):
        self.add_sequence(time, "roll", message, angle=angle)