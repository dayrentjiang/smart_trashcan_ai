import time
# import serial   # enable later on Pi with Nano
from config import SERIAL_PORT, BAUD_RATE

class ArduinoController:
    def __init__(self):
        # try:
        #     self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        #     time.sleep(2)
        #     print("[INFO] Connected to Arduino on", SERIAL_PORT)
        # except Exception as e:
        #     print("[DUMMY] Running in dummy mode:", e)
        self.ser = None

    def send(self, command: str):
        msg = command.strip() + "\n"
        if self.ser:
            self.ser.write(msg.encode("utf-8"))
            print(f"[INFO] Sent to Arduino: {command}")
        else:
            print(f"[DUMMY] Would send to Arduino: {command}")

    def read_line(self):
        if self.ser:
            if self.ser.in_waiting > 0:
                return self.ser.readline().decode("utf-8").strip()
            return None
        else:
            input("[DUMMY] Press ENTER to simulate IR trigger...")
            return "READY"

    def close(self):
        if self.ser:
            self.ser.close()
            print("[INFO] Arduino connection closed")
        else:
            print("[DUMMY] Closing dummy controller.")
