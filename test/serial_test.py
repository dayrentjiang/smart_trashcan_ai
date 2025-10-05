import serial
import time

# Change this to your Arduino port
PORT = "/dev/cu.usbserial-1110"
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # wait for Arduino to reset
print(f"[INFO] Connected to {PORT}")

try:
    while True:
        if ser.in_waiting > 0:
            msg = ser.readline().decode("utf-8", errors="ignore").strip()
            if msg:
                print(f"[FROM ARDUINO] {msg}")

                # reply automatically for test
                if msg == "READY":
                    ser.write(b"PLASTIC\n")
                    print("[TO ARDUINO] Sent: PLASTIC")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n[INFO] Closing serial port.")
    ser.close()
