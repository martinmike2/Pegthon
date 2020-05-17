import sys
from PyQt5.QtWidgets import QApplication

import Globals
from Connection import Connection
from Views import MainWindow

Globals.connection = Connection().get_conn("test", "10.0.4.10", [50000, 50001])
Globals.mu = Globals.connection.space_center.active_vessel.orbit.body.gravitation_parameter

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())
