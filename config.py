# config.py

# Mapping YOLO labels to compartments
CATEGORY_MAP = {
    "Glass": "glass_paper",
    "Paper": "glass_paper",
    "Metal": "metal",
    "Plastic": "plastic",
    "trash": "trash"
}

# Serial port settings (adjust if your Nano shows up differently)
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
