import serial
import time
import traceback

class ArduinoController:
    def __init__(self, port="/dev/cu.usbserial-1110", baud=9600, dummy=False):
        self.dummy = dummy
        self.ser = None

        print(f"[DEBUG] Initializing ArduinoController...")
        print(f"[DEBUG] Port: {port}, Baud: {baud}, Dummy mode: {self.dummy}")

        if not self.dummy:
            try:
                print("[DEBUG] Attempting to open serial port...")
                self.ser = serial.Serial(port, baud, timeout=1)
                time.sleep(2)
                if self.ser.is_open:
                    print(f"[INFO] ✅ Connected to Arduino on {port}")
                else:
                    print(f"[ERROR] ❌ Serial port {port} did not open.")
                    self.dummy = True
            except Exception as e:
                print(f"[ERROR] ❌ Could not connect to Arduino: {e}")
                traceback.print_exc()  # <-- full error details
                self.dummy = True
        else:
            print("[DUMMY] Running without Arduino connection")

    def send(self, command: str):
        msg = command.strip().upper() + "\n"
        print(f"[DEBUG] Preparing to send: '{msg.strip()}'")

        if self.ser:
            try:
                self.ser.write(msg.encode("utf-8"))
                print(f"[TO ARDUINO] Sent: {command}")
                time.sleep(0.1)

                while self.ser.in_waiting:
                    log = self.ser.readline().decode("utf-8", errors="ignore").strip()
                    if log:
                        print(f"[FROM ARDUINO] {log}")
            except Exception as e:
                print(f"[ERROR] ❌ Failed to send to Arduino: {e}")
                traceback.print_exc()
        else:
            print(f"[DUMMY] Would send: {command}")

    def read_line(self):
        if self.ser and self.ser.in_waiting:
            line = self.ser.readline().decode("utf-8", errors="ignore").strip()
            print(f"[DEBUG] Read line: {line}")
            return line
        return None

    def close(self):
        if self.ser:
            try:
                self.ser.close()
                print("[INFO] Closed Arduino serial port")
            except Exception as e:
                print(f"[ERROR] ❌ Failed to close port: {e}")
        else:
            print("[DEBUG] No serial connection to close")
