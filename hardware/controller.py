import serial
import time

class ArduinoController:
    def __init__(self, port="/dev/cu.usbserial-1110", baud=9600, dummy=False):
        self.dummy = dummy
        self.ser = None

        if not self.dummy:
            try:
                self.ser = serial.Serial(port, baud, timeout=1)
                time.sleep(2)
                print(f"[INFO] Connected to Arduino on {port}")
            except Exception as e:
                print(f"[ERROR] Could not connect to Arduino: {e}")
                self.dummy = True
        else:
            print("[DUMMY] Running without Arduino connection")

    def send(self, command: str):
        msg = command.strip().upper() + "\n"
        if self.ser:
            self.ser.write(msg.encode("utf-8"))
            print(f"[TO ARDUINO] Sent: {command}")

            # read back any Arduino logs for a short time
            time.sleep(0.1)
            while self.ser.in_waiting:
                log = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if log:
                    print(f"[FROM ARDUINO] {log}")
        else:
            print(f"[DUMMY] Would send: {command}")

    def read_line(self):
        # For now, we skip waiting for READY since no button
        return "READY"

    def close(self):
        if self.ser:
            self.ser.close()
            print("[INFO] Closed Arduino serial port")
