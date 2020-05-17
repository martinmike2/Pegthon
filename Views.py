import Globals
from Controls import Controls
from Mission import Mission
from Vehicle import Vehicle
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QDialogButtonBox, QLabel, QGridLayout

stages = []
sequences = []
controls = {}
mission = None
vehicle = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(626, 532)
        self.centralWidget = QtWidgets.QWidget(self)

        self.vhcSelect = QtWidgets.QComboBox(self.centralWidget)
        self.vhcSelect.setGeometry(QtCore.QRect(330, 40, 171, 26))
        self.vhcLabel = QtWidgets.QLabel(self.centralWidget)
        self.vhcLabel.setText("Vehicle")
        self.vhcLabel.setGeometry(QtCore.QRect(330, 20, 60, 16))
        self.vhcTable = QtWidgets.QTableWidget(self.centralWidget)
        self.vhcTable.setGeometry(QtCore.QRect(330, 70, 256, 301))
        self.vhcTable.setColumnCount(0)
        self.vhcTable.setRowCount(0)
        self.btnNewVhc = QtWidgets.QPushButton(self.centralWidget)
        self.btnNewVhc.setGeometry(QtCore.QRect(380, 10, 113, 32))
        self.btnNewVhc.setText("New Vehicle")

        self.msnLabel = QtWidgets.QLabel(self.centralWidget)
        self.msnLabel.setText("Mission")
        self.msnLabel.setGeometry(QtCore.QRect(10, 20, 60, 16))
        self.msnTable = QtWidgets.QTableWidget(self.centralWidget)
        self.msnTable.setGeometry(QtCore.QRect(10, 70, 256, 301))
        self.msnTable.setColumnCount(2)
        self.msnTable.setRowCount(0)
        self.msnSelect = QtWidgets.QComboBox(self.centralWidget)
        self.msnSelect.setGeometry(QtCore.QRect(10, 40, 171, 26))
        self.btnNewMsn = QtWidgets.QPushButton(self.centralWidget)
        self.btnNewMsn.setText("New Mission")
        self.btnNewMsn.setGeometry(QtCore.QRect(60, 10, 113, 32))

        self.btnLaunch = QtWidgets.QPushButton(self.centralWidget)
        self.btnLaunch.setGeometry(QtCore.QRect(10, 380, 601, 61))
        self.btnLaunch.setText("Launch")

        self.setCentralWidget(self.centralWidget)
        self.fill_dropdowns()
        self.make_connection()

    def fill_dropdowns(self):
        from os import listdir
        from os.path import isfile, join
        vehicles = [None]
        missions = [None]
        for f in listdir("vehicles"):
            if isfile(join("vehicles", f)):
                vehicles.append(f)
        for f in listdir("missions"):
            if isfile(join("missions", f)):
                missions.append(f)

        self.vhcSelect.addItems(vehicles)
        self.msnSelect.addItems(missions)

    def make_connection(self):
        self.btnNewMsn.clicked.connect(self.new_mission)
        self.btnNewVhc.clicked.connect(self.new_vehicle)
        self.msnSelect.currentTextChanged.connect(self.load_mission)
        self.vhcSelect.currentTextChanged.connect(self.load_vehicle)
        self.btnLaunch.clicked.connect(self.launch)

    def launch(self):
        global mission
        global vehicle
        Globals.mission = Mission(mission["apoapsis"], mission["periapsis"], mission["payload"], mission["inclination"],
                                  mission["lan"], mission["direction"])
        Globals.controls = Controls(mission["launch_time_advance"], mission["vertical_ascent_time"],
                                    mission["pitch_over_angle"], mission["upfg_activation"], mission["launch_azimuth"],
                                    mission["initial_roll"])
        Globals.vehicle = Vehicle()
        for stage in vehicle["stages"]:
            Globals.vehicle.add_stage(stage)
        for seq in vehicle["sequences"]:
            Globals.vehicle.add_sequence(seq)

    def load_mission(self, miss):
        import json

        if miss == '':
            self.msnTable.clear()
            return

        f = json.load(open("missions/" + miss, 'r'))
        global mission
        mission = f
        for key in f:
            value = f[key]
            row = self.msnTable.rowCount()
            self.msnTable.insertRow(row)
            self.msnTable.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            self.msnTable.setItem(row, 1, QtWidgets.QTableWidgetItem(value))

    def load_vehicle(self, veh):
        import json

        if veh == '':
            self.vhcTable.clear()
            return

        f = json.load(open("vehicles/" + veh, 'r'))
        global vehicle
        vehicle = f
        for key in f:
            value = f[key]
            row = self.vhcTable.rowCount()
            self.vhcTable.insertRow(row)
            self.msnTable.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
            self.msnTable.setItem(row, 1, QtWidgets.QTableWidgetItem(value))

    def new_mission(self):
        dlg = NewMissionWindow(self)
        dlg.exec_()

    def new_vehicle(self):
        dlg = NewVehicleWindow(self)
        dlg.exec_()


class NewMissionWindow(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(NewMissionWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("New Mission")
        self.resize(260, 290)

        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 201, 221))

        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.nameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nameLabel.setText("Mission Name")
        self.nameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)

        self.payloadLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.payloadLabel.setText("Payload")
        self.payloadLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.payloadLabel)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.payloadLineEdit)

        self.periapsisLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.periapsisLabel.setText("Periapsis")
        self.periapsisLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.periapsisLabel)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.periapsisLineEdit)

        self.apoapsisLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.apoapsisLabel.setText("Apoapsis")
        self.apoapsisLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.apoapsisLabel)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.apoapsisLineEdit)

        self.altitudeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.altitudeLabel.setText("Altitude")
        self.altitudeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.altitudeLabel)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.altitudeLineEdit)
        #
        self.inclinationLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.inclinationLabel.setText("Inclination")
        self.inclinationLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.inclinationLabel)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.inclinationLineEdit)

        self.lanLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.lanLabel.setText("LAN")
        self.lanLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lanLabel)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lanLineEdit)

        self.directionLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.directionLabel.setText("Direction")
        self.directionComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.directionLabel)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.directionComboBox)
        self.directionComboBox.addItems(["North", "South", "Nearest"])

        self.launchTimeAdvanceLabel = QLabel(self.formLayoutWidget)
        self.launchTimeAdvanceLabel.setText("Launch Time Advance")
        self.launchTimeAdvanceSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.launchTimeAdvanceSpinBox.setMaximum(10000)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.launchTimeAdvanceLabel)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.launchTimeAdvanceSpinBox)

        self.verticalAscentTimeLabel = QLabel(self.formLayoutWidget)
        self.verticalAscentTimeLabel.setText("Vertical Ascent TIme")
        self.verticalAscentTimeSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.verticalAscentTimeLabel)
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.verticalAscentTimeSpinBox)

        self.pitchOverAngleLabel = QLabel(self.formLayoutWidget)
        self.pitchOverAngleLabel.setText("Pitch Over Angle")
        self.pitchOverAngleSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.pitchOverAngleSpinBox.setMaximum(20)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.pitchOverAngleLabel)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.pitchOverAngleSpinBox)

        self.upfgActivationLabel = QLabel(self.formLayoutWidget)
        self.upfgActivationLabel.setText("UPFG Activation MET")
        self.upfgActivationSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.upfgActivationSpinBox.setMaximum(10000)
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.upfgActivationLabel)
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.upfgActivationSpinBox)

        self.azg = QtWidgets.QGroupBox(self.formLayoutWidget)
        azh = QtWidgets.QHBoxLayout(self.azg)
        azh.setSpacing(10)
        self.azg.setLayout(azh)
        self.launchAzimuthLabel = QLabel(self.formLayoutWidget)
        self.launchAzimuthLabel.setText("Launch Azimuth")
        self.launchAzimuthEnable = QtWidgets.QCheckBox(self.formLayoutWidget)
        azh.addWidget(self.launchAzimuthEnable)
        azh.addWidget(self.launchAzimuthLabel)
        self.launchAzimuthSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.launchAzimuthSpinBox.setSingleStep(0.01)
        self.launchAzimuthSpinBox.setMinimum(-90)
        self.launchAzimuthSpinBox.setMaximum(90)
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.azg)
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.launchAzimuthSpinBox)

        self.rg = QtWidgets.QGroupBox(self.formLayoutWidget)
        rh = QtWidgets.QHBoxLayout(self.rg)
        rh.setSpacing(10)
        self.azg.setLayout(rh)
        self.initialRollLabel = QLabel(self.formLayoutWidget)
        self.initialRollLabel.setText("Initial Roll")
        self.initialRollEnable = QtWidgets.QCheckBox(self.formLayoutWidget)
        rh.addWidget(self.initialRollEnable)
        rh.addWidget(self.initialRollLabel)
        self.initialRollSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.initialRollSpinBox.setMaximum(180)
        self.initialRollSpinBox.setMinimum(-180)
        self.initialRollSpinBox.setSingleStep(1)
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.rg)
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.initialRollSpinBox)

        self.buttonbox = QtWidgets.QDialogButtonBox(self.formLayoutWidget)
        self.buttonbox.setGeometry(QtCore.QRect(30, 250, 201, 32))
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.rejected)

        self.layout = QtWidgets.QFormLayout()
        self.layout.addWidget(self.formLayoutWidget)
        self.layout.addWidget(self.buttonbox)
        self.setLayout(self.layout)

    def accept(self):
        import json
        result = {
            "payload": float(self.payloadLineEdit.text()),
            "apoapsis": float(self.apoapsisLineEdit.text()),
            "periapsis": float(self.periapsisLineEdit.text()),
            "inclination": None,
            "altitude": None,
            "lan": None,
            "direction": self.directionComboBox.currentText()
        }

        if self.altitudeLineEdit.text() != '':
            result["altitude"] = float(self.altitudeLineEdit.text())
        if self.inclinationLineEdit.text() != '':
            result["inclination"] = float(self.inclinationLineEdit.text())
        if self.lanLineEdit.text() != '':
            result["lan"] = float(self.lanLineEdit.text())

        result["launch_time_advance"] = self.launchTimeAdvanceSpinBox.value()
        result["vertical_ascent_time"] = self.verticalAscentTimeSpinBox.value()
        result["pitch_over_angle"] = self.pitchOverAngleSpinBox.value()
        result["upfg_activation"] = self.upfgActivationSpinBox.value()

        if self.launchAzimuthEnable.isChecked():
            result["launch_azimuth"] = self.launchAzimuthSpinBox.value()
        else:
            result["launch_azimuth"] = None
        if self.initialRollEnable.isChecked():
            result["initial_roll"] = self.initialRollSpinBox.value()
        else:
            result["initial_roll"] = None

        with open("missions/" + self.nameLineEdit.text() + ".json", "w") as f:
            f.write(json.dumps(result))

        self.close()


class NewVehicleWindow(QtWidgets.QDialog):
    vehicle = None

    def __init__(self, *args, **kwargs):
        super(NewVehicleWindow, self).__init__(*args, **kwargs)
        self.resize(630, 306)
        self.formLayoutWidget = QtWidgets.QWidget(self)

        self.gridLayout = QtWidgets.QGridLayout(self.formLayoutWidget)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.formLayoutWidget)
        self.buttonBox.setGeometry(QtCore.QRect(250, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)

        self.stagesLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.stagesLabel.setGeometry(QtCore.QRect(50, 20, 60, 16))
        self.stagesLabel.setText("Stages")
        self.gridLayout.addWidget(self.stagesLabel, 0, 0)

        self.stagesList = QtWidgets.QListWidget(self.formLayoutWidget)
        self.stagesList.setGeometry(QtCore.QRect(110, 20, 431, 101))
        self.gridLayout.addWidget(self.stagesList, 0, 1)

        self.btnAddStage = QtWidgets.QPushButton(self.formLayoutWidget)
        self.btnAddStage.setGeometry(QtCore.QRect(550, 20, 41, 32))
        self.btnAddStage.setText("+")

        self.btnRemStage = QtWidgets.QPushButton(self.formLayoutWidget)
        self.btnRemStage.setGeometry(QtCore.QRect(550, 90, 41, 32))
        self.btnRemStage.setText("-")

        self.stageBtnLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
        self.gridLayout.addLayout(self.stageBtnLayout, 0, 2)
        self.stageBtnLayout.addWidget(self.btnAddStage, 0)
        self.stageBtnLayout.addWidget(self.btnRemStage, 1)

        self.seqLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.seqLabel.setText("Sequence")
        self.seqLabel.setGeometry(QtCore.QRect(40, 140, 60, 16))
        self.gridLayout.addWidget(self.seqLabel, 1, 0)

        self.seqList = QtWidgets.QListWidget(self.formLayoutWidget)
        self.seqList.setGeometry(QtCore.QRect(110, 140, 431, 101))
        self.gridLayout.addWidget(self.seqList, 1, 1)

        self.seqAddBtn = QtWidgets.QPushButton(self.formLayoutWidget)
        self.seqAddBtn.setText("+")
        self.seqAddBtn.setGeometry(QtCore.QRect(550, 140, 41, 32))

        self.seqRemBtn = QtWidgets.QPushButton(self.formLayoutWidget)
        self.seqRemBtn.setText("-")
        self.seqRemBtn.setGeometry(QtCore.QRect(550, 210, 41, 32))

        self.seqBtnLayout = QtWidgets.QVBoxLayout(self.formLayoutWidget)
        self.gridLayout.addLayout(self.seqBtnLayout, 1, 2)
        self.seqBtnLayout.addWidget(self.seqAddBtn, 0)
        self.seqBtnLayout.addWidget(self.seqRemBtn, 1)

        self.layout = QtWidgets.QFormLayout()
        self.layout.addWidget(self.formLayoutWidget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.btnAddStage.clicked.connect(self.new_stage)
        self.btnRemStage.clicked.connect(self.rem_stage)
        self.seqAddBtn.clicked.connect(self.new_sequence)
        self.seqRemBtn.clicked.connect(self.rem_sequence)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.vehicle = {}

    def new_stage(self):
        dlg = NewStageWindow(self)
        r = dlg.exec_()
        if r:
            global stages
            stages.append(dlg.stage)
            self.stagesList.clear()
            for stage in stages:
                self.stagesList.addItem(stage["name"])

    def rem_stage(self):
        self.stagesList.clear()
        global stages
        del stages[-1]
        for stage in stages:
            self.stagesList.addItem(stage["name"])

    def new_sequence(self):
        dlg = NewSequenceWindow(self)
        r = dlg.exec_()

        if r:
            global sequences
            sequences.append(dlg.sequence)
            sequences.sort(key=self.by_time)
            self.seqList.clear()
            for seq in sequences:
                self.seqList.addItem("{0} | {1} | {2}".format(seq["time"], seq["type"], seq["value"]))

    def rem_sequence(self):
        self.seqList.clear()
        global sequences
        del sequences[-1]
        self.seqList.clear()
        for seq in sequences:
            self.seqList.addItem("{0} | {1} | {2}".format(seq["time"], seq["type"], seq["value"]))

    def by_time(self, elem):
        return elem["time"]

    def accept(self) -> None:
        global stages
        global sequences
        global controls

        self.vehicle["stages"] = stages
        self.vehicle["sequence"] = sequences

        super().accept()


class NewStageWindow(QtWidgets.QDialog):
    stage = {}

    def __init__(self, *args, **kwargs):
        super(NewStageWindow, self).__init__(*args, **kwargs)
        self.resize(884, 718)

        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QRect(10, 10, 501, 663))

        self.gridLayout = QGridLayout(self.formLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout2 = QGridLayout(self.formLayoutWidget)

        self.buttonbox = QDialogButtonBox(self.formLayoutWidget)
        self.buttonbox.setGeometry(QRect(110, 680, 342, 32))
        self.buttonbox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.jettisonLabel = QLabel(self.formLayoutWidget)
        self.jettisonLabel.setText("Jettison")
        self.gridLayout2.addWidget(self.jettisonLabel, 0, 0, 1, 1)

        self.jettisonCheckbox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.gridLayout2.addWidget(self.jettisonCheckbox, 0, 1, 1, 1)

        self.waitForJettisonLabel = QLabel(self.formLayoutWidget)
        self.waitForJettisonLabel.setText("Wait for Jettison")
        self.gridLayout2.addWidget(self.waitForJettisonLabel, 1, 0, 1, 1)

        self.waitForJettisonSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.waitForJettisonSpinBox.setSuffix("s")
        self.gridLayout2.addWidget(self.waitForJettisonSpinBox, 1, 1, 1, 1)

        self.ignitionLabel = QLabel(self.formLayoutWidget)
        self.ignitionLabel.setText("Ignition")
        self.gridLayout2.addWidget(self.ignitionLabel, 2, 0, 1, 1)

        self.ignitionCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.gridLayout2.addWidget(self.ignitionCheckBox, 2, 1, 1, 1)

        self.waitBeforeIgnitionLabel = QLabel(self.formLayoutWidget)
        self.waitBeforeIgnitionLabel.setText("Wait before Ignition")
        self.gridLayout2.addWidget(self.waitBeforeIgnitionLabel, 3, 0, 1, 1)

        self.waitBeforeIgnitionSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.waitBeforeIgnitionSpinBox.setSuffix("s")
        self.gridLayout2.addWidget(self.waitBeforeIgnitionSpinBox, 3, 1, 1, 1)

        self.ullageLabel = QLabel(self.formLayoutWidget)
        self.ullageLabel.setText("Requires Ullage")
        self.gridLayout2.addWidget(self.ullageLabel, 4, 0, 1, 1)

        self.ullageCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.gridLayout2.addWidget(self.ullageCheckBox, 4, 1, 1, 1)

        self.ullageBurnDurationLabel = QLabel(self.formLayoutWidget)
        self.ullageBurnDurationLabel.setText("Ullage Burn Duration")
        self.gridLayout2.addWidget(self.ullageBurnDurationLabel, 5, 0, 1, 1)

        self.ullageBurnDurationSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.ullageBurnDurationSpinBox.setSuffix("s")
        self.gridLayout2.addWidget(self.ullageBurnDurationSpinBox, 5, 1, 1, 1)

        self.postUllageBurnLabel = QLabel(self.formLayoutWidget)
        self.postUllageBurnLabel.setText("Post Ullage Burn")
        self.gridLayout2.addWidget(self.postUllageBurnLabel, 6, 0, 1, 1)

        self.postUllageBurnSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.postUllageBurnSpinBox.setSuffix("s")
        self.gridLayout2.addWidget(self.postUllageBurnSpinBox, 6, 1, 1, 1)

        self.nameLabel = QLabel(self.formLayoutWidget)
        self.nameLabel.setText("Name")
        self.gridLayout.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.nameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gridLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)

        self.totalMassLabel = QLabel(self.formLayoutWidget)
        self.totalMassLabel.setText("Total Mass")
        self.gridLayout.addWidget(self.totalMassLabel, 1, 0, 1, 1)

        self.totalMassLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gridLayout.addWidget(self.totalMassLineEdit, 1, 1, 1, 1)

        self.fuelMassLabel = QLabel(self.formLayoutWidget)
        self.fuelMassLabel.setText("Fuel Mass")
        self.gridLayout.addWidget(self.fuelMassLabel, 2, 0, 1, 1)

        self.fuelMassLineEdit = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.fuelMassLineEdit, 2, 1, 1, 1)

        self.dryMassLabel = QLabel(self.formLayoutWidget)
        self.dryMassLabel.setText("Dry Mass")
        self.gridLayout.addWidget(self.dryMassLabel, 3, 0, 1, 1)

        self.dryMassLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gridLayout.addWidget(self.dryMassLineEdit, 3, 1, 1, 1)

        self.gLimitLabel = QLabel(self.formLayoutWidget)
        self.gLimitLabel.setText("G Limit")
        self.gridLayout.addWidget(self.gLimitLabel, 4, 0, 1, 1)

        self.gLimitLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.gridLayout.addWidget(self.gLimitLineEdit, 4, 1, 1, 1)

        self.minimumThrottleLabel = QLabel(self.formLayoutWidget)
        self.minimumThrottleLabel.setText("Minimum Throttle")
        self.gridLayout.addWidget(self.minimumThrottleLabel, 5, 0, 1, 1)

        self.minimumThrottleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.minimumThrottleSpinBox.setMaximum(1)
        self.minimumThrottleSpinBox.setSingleStep(0.1)
        self.minimumThrottleSpinBox.setMinimum(0)
        self.gridLayout.addWidget(self.minimumThrottleSpinBox, 5, 1, 1, 1)

        self.throttleLabel = QLabel(self.formLayoutWidget)
        self.throttleLabel.setText("Throttle")
        self.gridLayout.addWidget(self.throttleLabel, 6, 0, 1, 1)

        self.throttleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.throttleSpinBox.setMinimum(0)
        self.throttleSpinBox.setMaximum(1)
        self.throttleSpinBox.setSingleStep(0.1)
        self.gridLayout.addWidget(self.throttleSpinBox, 6, 1, 1, 1)

        self.shutdownRequiredLabel = QLabel(self.formLayoutWidget)
        self.shutdownRequiredLabel.setText("Shutdown Required")
        self.gridLayout.addWidget(self.shutdownRequiredLabel, 7, 0, 1, 1)

        self.shutdownRequiredCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.gridLayout.addWidget(self.shutdownRequiredCheckBox, 7, 1, 1, 1)

        self.engineLabel = QLabel(self.formLayoutWidget)
        self.engineLabel.setText("Engines")
        self.gridLayout.addWidget(self.engineLabel, 8, 0, 1, 1)

        self.engineTable = QtWidgets.QTableWidget(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.engineTable.sizePolicy().hasHeightForWidth())
        self.engineTable.setSizePolicy(sizePolicy)
        self.engineTable.setColumnCount(3)
        self.engineTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText("ISP")
        self.engineTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Thrust")
        self.engineTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Flow")
        self.engineTable.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.engineTable, 8, 1, 1, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.engineAddButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.engineDelButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.engineAddButton.setText("+")
        self.engineDelButton.setText("-")
        self.verticalLayout.addWidget(self.engineAddButton)
        self.verticalLayout.addWidget(self.engineDelButton)
        self.gridLayout.addLayout(self.verticalLayout, 8, 2, 1, 1)

        self.stagingLabel = QLabel(self.formLayoutWidget)
        self.stagingLabel.setText("Staging")
        self.gridLayout.addWidget(self.stagingLabel, 9, 0, 1, 1)

        self.gridLayout.addWidget(self.buttonbox, 10, 1, 1, 1)

        self.gridLayout.addLayout(self.gridLayout2, 9, 1, 1, 1)
        self.setLayout(self.gridLayout)

        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        self.engineAddButton.clicked.connect(self.new_engine)
        self.engineDelButton.clicked.connect(self.rem_engine)

    def new_engine(self):
        rowPosition = self.engineTable.rowCount()
        self.engineTable.insertRow(rowPosition)

    def rem_engine(self):
        rowPosition = self.engineTable.rowCount() - 1
        self.engineTable.removeRow(rowPosition)

    def accept(self) -> None:
        import Globals
        ret = {
            "name": self.nameLineEdit.text()
        }

        mt = self.totalMassLineEdit.text()
        mf = self.fuelMassLineEdit.text()
        md = self.dryMassLineEdit.text()
        glim = self.gLimitLineEdit.text()
        mthr = self.minimumThrottleSpinBox.value()
        thr = self.throttleSpinBox.value()
        sht = self.shutdownRequiredCheckBox.text()

        if mt == '' and mf != '' and md != '':
            mf = float(mf)
            md = float(mf)
            mt = mf + md
        elif mf == '' and mt != '' and md != '':
            mt = float(mt)
            md = float(md)
            mf = mt - md
        elif md == '' and mt != '' and mf != '':
            mt = float(mt)
            mf = float(mf)
            md = mt - mf
        else:
            raise Exception("Must specify at least 2 of: Total Mass, Mass Fuel, Dry Mass")

        ret["mass_total"] = mt
        ret["mass_fuel"] = mf
        ret["mass_dry"] = md
        ret["minimum_throttle"] = float(mthr)

        if thr == 0:
            thr = 1.0

        if glim == '':
            glim = None
        else:
            glim = float(glim)

        ret['g_lim'] = glim
        ret['shutdown_required'] = bool(sht)
        ret["throttle"] = thr

        rows = self.engineTable.rowCount()
        engines = []
        for i in range(0, rows):
            isp = self.engineTable.item(i, 0).text()
            thrust = self.engineTable.item(i, 1).text()
            flow = self.engineTable.item(i, 2)

            if isp == '' or thrust == '':
                raise Exception("You must specify ISP and Thrust")

            thrust = float(thrust)
            isp = float(isp)

            if flow is None or flow.text() == '':
                flow = thrust / (isp * Globals.g0) * thr
            else:
                flow = float(flow.text())

            engine = {
                "isp": float(isp),
                "thrust": float(thrust),
                "flow": float(flow)
            }
            engines.append(engine)

        ret["engines"] = engines

        staging = {
            "jettison": bool(self.jettisonCheckbox.text()),
            "ignition": bool(self.ignitionCheckBox.text()),
            "wait_before_jettison": self.waitForJettisonSpinBox.value(),
            "wait_before_ignition": self.waitBeforeIgnitionSpinBox.value(),
            "ullage": bool(self.ullageCheckBox.text()),
            "ullage_burn_duration": self.ullageBurnDurationSpinBox.value(),
            "post_ullage_burn": self.postUllageBurnSpinBox.value()
        }

        ret["staging"] = staging

        self.stage = ret

        super().accept()


class NewSequenceWindow(QtWidgets.QDialog):
    sequence = None
    prev_type = None

    massLostLabel = None
    massLostLineEdit = None
    throttleSettingLabel = None
    throttleSettingSpinBox = None
    rollLabel = None
    rollSpinBox = None

    def __init__(self, *args, **kwargs):
        super(NewSequenceWindow, self).__init__(*args, **kwargs)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.addons = []

        self.timeLabel = QLabel(self)
        self.timeLabel.setText("Time after Liftoff")
        self.timeSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.timeSpinBox.setSingleStep(0.5)
        self.timeSpinBox.setMinimum(-360000)
        self.timeSpinBox.setSuffix("s")
        self.gridLayout.addWidget(self.timeLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.timeSpinBox, 0, 1, 1, 1)

        self.typeLabel = QLabel(self)
        self.typeLabel.setText("Type")
        self.typeComboBox = QtWidgets.QComboBox(self)
        self.typeComboBox.addItems([None, "print", "stage", "jettison", "throttle", "roll"])
        self.gridLayout.addWidget(self.typeLabel, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.typeComboBox, 1, 1, 1, 1)

        self.messageLabel = QLabel(self)
        self.messageLabel.setText("Message")
        self.messageLineEdit = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.messageLabel, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.messageLineEdit, 2, 1, 1, 1)

        self.bottomContainer = QtWidgets.QWidget(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.typeComboBox.activated.connect(self.type_combo)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.rejected)
        self.sequence = {}

    def type_combo(self):
        type = self.typeComboBox.currentText()

        if self.prev_type == "jettison":
            self.gridLayout.removeWidget(self.massLostLabel)
            self.gridLayout.removeWidget(self.massLostLineEdit)
            self.massLostLabel.deleteLater()
            self.massLostLineEdit.deleteLater()
        elif self.prev_type == "throttle":
            self.gridLayout.removeWidget(self.throttleSettingLabel)
            self.gridLayout.removeWidget(self.throttleSettingSpinBox)
            self.throttleSettingLabel.deleteLater()
            self.throttleSettingSpinBox.deleteLater()
        elif self.prev_type == "roll":
            self.gridLayout.removeWidget(self.rollLabel)
            self.gridLayout.removeWidget(self.rollSpinBox)
            self.rollLabel.deleteLater()
            self.rollSpinBox.deleteLater()

        if type == "jettison":
            self.jettison_type()
        elif type == "throttle":
            self.throttle_type()
        elif type == "roll":
            self.roll_type()

        self.prev_type = type
        self.gridLayout.update()

    def jettison_type(self):
        self.massLostLabel = QLabel(self)
        self.massLostLabel.setText("Mass Lost")
        self.massLostLineEdit = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.massLostLabel, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.massLostLineEdit, 3, 1, 1, 1)

    def throttle_type(self):
        self.throttleSettingLabel = QLabel(self)
        self.throttleSettingLabel.setText("Throttle Setting")
        self.throttleSettingSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.throttleSettingSpinBox.setSingleStep(0.01)
        self.throttleSettingSpinBox.setSuffix("%")
        self.throttleSettingSpinBox.setMinimum(0)
        self.throttleSettingSpinBox.setMaximum(1)
        self.gridLayout.addWidget(self.throttleSettingLabel, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.throttleSettingSpinBox, 3, 1, 1, 1)

    def roll_type(self):
        self.rollLabel = QLabel(self.addonContainer)
        self.rollLabel.setText("Roll Angle")
        self.rollSpinBox = QtWidgets.QSpinBox(self.addonContainer)
        self.rollSpinBox.setMaximum(180)
        self.rollSpinBox.setMinimum(-180)
        self.gridLayout.addWidget(self.rollLabel, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.rollSpinBox, 3, 1, 1, 1)

    def accept(self) -> None:
        type = self.typeComboBox.currentText()
        self.sequence["time"] = float(self.timeSpinBox.value())
        self.sequence["type"] = type
        self.sequence["message"] = self.messageLineEdit.text()

        if type == "jettison":
            self.sequence["value"] = float(self.massLostLineEdit.text())
        elif type == "throttle":
            self.sequence["value"] = self.throttleSettingSpinBox.value()
        elif type == "roll":
            self.sequence["value"] = self.rollSpingBox.value()
        else:
            self.sequence["value"] = None

        super().accept()
