class ServoController:
    def __init__(self):
        print("Dummy servo initialized (Mac mode).")

    def move(self, decision):
        if decision == "recyclable":
            print("Servo would move LEFT → recyclable bin")
        else:
            print("Servo would move RIGHT → non-recyclable bin")
