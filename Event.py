class Event:
    def __init__(self, first, second = None, type = None, time = 0, keep = False, move = 0):
        self.first = first
        self.second = second

        self.set_state(type, time, keep)

    def set_state(self, type = None, time = 0, keep = None):
        if not type: # If it's the confirmation sort
            self.type = "comparison"
            self.time = 0.025
            self.keep = True
        else:
            self.type = type
            self.time = time
            self.keep = keep

    @property
    def color(self):
        color_dict = {
            "comparison": 'green',
            "swap": 'red'
        }
        return color_dict[self.type]

    def __repr__(self):
        return f"Event({self.first=}, {self.second=}, {self.type=})\n"

    @staticmethod
    def calculate_time(length):
        return Event.MAX_TIME