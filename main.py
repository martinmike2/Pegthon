import Globals
from Connection import Connection
from Mission import Mission
from Controls import Controls
import json
import sys

Globals.connection = Connection().get_conn("test", "192.168.1.7", [50000, 50001])
Globals.mission = Mission(200, 200, 1000, None, 53)
Globals.controls = Controls(150, 7, 10, 115)
Globals.mu = Globals.connection.space_center.active_vessel.orbit.body.gravitation_parameter

mission = sys.argv[0]

fp =open("./missions/"+mission+'.json')
mission = json.load(fp)
vehicle = mission["vehicle"]

print(vehicle)
