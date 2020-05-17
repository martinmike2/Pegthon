import math
import Globals
import helpers
from Vector3 import Vector3


class Mission:
    def __init__(self, apoapsis=0, periapsis=0, payload=None, altitude=None, inclination=None, lan=None, direction=None):
        self.apoapsis = apoapsis
        self.periapsis = periapsis
        self.payload = payload
        self.altitude = altitude
        self.inclination = inclination
        self.lan = lan
        self.direction = direction

        if altitude is not None:
            if altitude < periapsis or altitude < apoapsis:
                self.altitude = periapsis
        else:
            self.altitude = periapsis

        if direction is None:
            self.direction = "nearest"

        if inclination is not None:
            while inclination < -180:
                inclination += 360
            while inclination > 180:
                inclination -= 360
            self.inclination = inclination
        else:
            self.inclination = math.fabs(Globals.connection.space_center.active_vessel.flight().latitude)

        if lan is not None:
            while lan < 0:
                lan += 360
            if lan > 360:
                lan = lan % 360
            self.lan = lan
        else:
            if self.direction == "nearest":
                self.direction = "north"
            current_node = helpers.node_vector(self.inclination, self.direction)
            current_lan = current_node.ang(helpers.solar_prime_vector(Globals.connection.space_center.active_vessel.orbit.body.reference_frame))

            if Vector3(0,1,0).dot(current_node.cross(helpers.solar_prime_vector)) < 0:
                current_lan = 360 - current_lan

            self.lan = current_lan + (Globals.controls.launchTimeAdvance + 30) / Globals.connection.space_center.active_vessel.orbit.body.rotational_period * 360
