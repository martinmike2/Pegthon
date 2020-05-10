import Globals
from Connection import Connection
from Mission import Mission
from Controls import Controls

Globals.connection = Connection().get_conn("test", "192.168.1.7", [50000, 50001])
Globals.mission = Mission(200, 200, 1000, None, 53)
Globals.controls = Controls(150, 7, 10, 115)

import helpers
helpers.orbit_time_intercept("nearest")