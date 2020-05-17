import Globals


class EventManager:
    staging: bool = False
    system_firing: bool = False
    user_firing: bool = False
    system_event_pointer: int = -1
    user_event_pointer: int = -1
    system_events: list = []
    user_events: list = []

    def __init__(self):
        time_to_launch = Globals.liftoff_time - Globals.current()

        if time_to_launch > 18000: self.add_event("system", -18000, "print", "5 hours to launch", None)
        if time_to_launch > 3600: self.add_event("system", -3600, "print", "1 hours to launch", None)
        if time_to_launch > 1800: self.add_event("system", -1800, "print", "30 minutes to launch", None)
        if time_to_launch > 600: self.add_event("system", -600, "print", "10 minutes to launch", None)
        if time_to_launch > 300: self.add_event("system", -300, "print", "5 minutes to launch", None)
        if time_to_launch > 60: self.add_event("system", -60, "print", "1 minute to launch", None)
        if time_to_launch > 30: self.add_event("system", -30, "print", "30 seconds to launch", None)
        self.add_event("system", -10, "print", "10 SECONDS TO LAUNCH", None)
        self.add_event("system", -9, "print", "9 SECONDS TO LAUNCH", None)
        self.add_event("system", -8, "print", "8 SECONDS TO LAUNCH", None)
        self.add_event("system", -7, "print", "7 SECONDS TO LAUNCH", None)
        self.add_event("system", -6, "print", "6 SECONDS TO LAUNCH", None)
        self.add_event("system", -5, "print", "5 SECONDS TO LAUNCH", None)
        self.add_event("system", -4, "print", "4 SECONDS TO LAUNCH", None)
        self.add_event("system", -3, "print", "3 SECONDS TO LAUNCH", None)
        self.add_event("system", -2, "print", "2 SECONDS TO LAUNCH", None)
        self.add_event("system", -1, "print", "1 SECONDS TO LAUNCH", None)

        self.handle_events()

    def add_event(self, etype, time, type, message, value):
        def make_event(time, type, message, value):
            event = {
                "time": time,
                "type": type,
                "message": message,
            }

            if type == "jettison":
                event["data"] = {"mass_lost": value}
            elif type == "throttle":
                event["data"] = {"throttle": value}
            elif type == "roll":
                event["data"] = {"angle", value}
            else:
                event["data"] = {}

            return event

        if etype == "system":
            self.system_events.append(make_event(time, type, message, value))
        elif etype == "user":
            self.user_events.append(make_event(time, type, message, value))

    def handle_events(self):
        self.do_system_events()
        self.do_user_events()

    def do_system_events(self):
        if self.system_event_pointer == -1:
            self.system_event_pointer = 1
            return




    def do_user_events(self):
        pass

    def execute_event(self, type, index):
        event = None
        if type == "system":
            event = self.system_events[index]
        elif type == "user":
            event = self.user_events[index]
        if event is None:
            return

        if event["type"] == "print":
            print(event["message"])
            return True
        elif event["type"] == " stage":
            Globals.connection.space_center().active_vessel.controls.activate_next_stage()
            return True
        elif event["type"] == "jettison":
            dm = event["value"]
            for stage in Globals.vehicle.stages:
                stage.massTotal -= dm
                stage.massDry -= dm
            Globals.connection.space_center().active_vessel.controler.activate_next_stage()
        elif event["type"] == "roll":
            Globals.connection.space_center().active_vessel.autopilot.roll(event["value"])

        if type == "system":
            self.system_events.remove(event)
        elif type == "user":
            self.user_events.remove(event)