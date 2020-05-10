from Connection import Connection
from Mission import Mission
from Vehicle import Vehicle
from Vehicle import Stage
from Vehicle import State
from Controls import Controls
from Target import Target


g0 = 9.80655
connection = None
mission: Mission = None
controls: Controls = None
target: Target = None
state: State = None
previous: State = None
vehicle: Vehicle = None
