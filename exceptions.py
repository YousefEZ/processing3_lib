class WidgetNameTakenException(Exception):
    def __init__(self):
        super().__init__("This Widget Key has been taken")

class WidgetNonExistentException(Exception):
    def __init__(self):
        super().__init__("This Widget does not exist.")

class UnrecognisedStateException(Exception):
    def __init__(self):
        super().__init__("The setting you wish to adjust does not exist.")
