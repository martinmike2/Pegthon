import math
import numpy as np
import Globals


def unit_vector(v):
    if v is tuple:
        v = np.array([v[0], v[1], v[2]])
    return v / np.linalg.norm(v)


def project(v1, v2):
    top = v1.dot(v2)
    bot = v2.dot(v2)
    return (top / bot) * v2


def angle(v1, v2):
    return math.acos(
        v1.dot(v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    )


def rad_to_deg(rad):
    return rad * (180 / math.pi)


def rodrigues(in_vector, axis, angle):
    axis = unit_vector(axis)
    out_vector = in_vector * math.cos(angle)
    out_vector = out_vector + axis * axis.dot(in_vector) * (1 - math.cos(angle))

    return out_vector


def vec_yz(input):
    return np.array([input[0], input[2], input[1]])


def const_acc_burn_time(stage):
    eng_data = stage.get_thrust()
    isp = eng_data[2]
    base_flow = eng_data[1]
    mass = stage.massTotal
    fuel = stage.massFuel
    glim = stage.gLim
    tmin = stage.minThrottle

    max_burn_time = isp / glim * math.log(mass / (mass - fuel))

    if tmin == 0:
        return max_burn_time

    violation_time = -isp / glim * math.log(tmin)
    const_thrust_time = 0
    if violation_time < max_burn_time:
        burned_fuel = mass * (1 - math.e ** (-glim / isp * violation_time))
        const_thrust_time = (fuel - burned_fuel) / (base_flow * tmin)

    return max_burn_time + const_thrust_time


def node_vector(inc, dir):
    conn = Globals.connection
    b = math.tan(90 - inc) * math.tan(conn.space_center.active_vessel.flight().latitude)
    b = math.asin(min(max(-1, b), 1))

    longitude_vector = project(
        np.array([0, 1, 0]),
        -unit_vector(conn.space_center.active_vessel.orbit.position_at(
            conn.space_center.ut,
            conn.space_center.active_vessel.orbit.body.reference_frame
        ))
    )
    if dir == "north":
        return rodrigues(longitude_vector, np.array([0, 1, 0]), b)
    elif dir == "south":
        return rodrigues(longitude_vector, np.array([0, 1, 0]), 180 - b)
    else:
        return node_vector(inc, "north")


def solar_prime_vector(reference_frame):
    conn = Globals.connection
    sun = conn.space_center.bodies["Sun"]
    second_per_degree = sun.rotational_speed / 360
    rotation_offset = np.mod(conn.space_center.ut / second_per_degree, 360)
    sun_position = sun.position(reference_frame)
    sun_position_2 = sun.surface_position(
        0, 0 - rotation_offset, reference_frame
    )

    prime_vector = np.asarray(sun_position_2) - np.asarray(sun_position)

    return unit_vector(prime_vector)


def orbit_time_intercept(dir):
    target_inc = Globals.mission.inclination
    target_lan = Globals.mission.lan

    if dir == "nearest":
        time_to_northerly = orbit_time_intercept(Globals.mission, "north")
        time_to_southerly = orbit_time_intercept(Globals.mission, "south")
        if time_to_southerly < time_to_northerly:
            Globals.mission.direction = "south"
            return time_to_southerly
        else:
            Globals.mission.direction = "north"
            return time_to_northerly
    else:
        current_node = node_vector(target_inc, dir)
        target_node = rodrigues(solar_prime_vector(
            Globals.connection.space_center.active_vessel.orbit.body.reference_frame
        ), np.array([0, 1, 0]), -target_lan)

        node_delta = angle(current_node, target_node)
        delta_dir = np.array([0, 1, 0]).dot(target_node.cross(current_node))

        if delta_dir < 0:
            node_delta = 360 - node_delta

        delta_time = Globals.connection.space_center.active_vessel.orbit.body.rotational_period * node_delta / 360

        return delta_time
