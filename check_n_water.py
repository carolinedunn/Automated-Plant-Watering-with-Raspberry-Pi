import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import OutputDevice

# --- CONFIGURATION ---
# GPIO 17 corresponds to Pin 11 on the header
PUMP_PIN = 17

# Set threshold based on your plant's needs (e.g., 30% moisture)
MOISTURE_THRESHOLD = 30.0 

# Duration to run the pump in seconds
WATERING_DURATION = 1.0 

# --- CALIBRATION CONSTANTS (From your measurements) ---
V_DRY = 2.0
V_WET = 1.0

# --- HARDWARE INITIALIZATION ---
# Initialize I2C and ADC
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads.gain = 1
    # Using '0' directly to avoid the namespace attribute error
    chan = AnalogIn(ads, 0)
except Exception as e:
    print(f"Error initializing ADC: {e}")
    exit(1)

# Initialize Pump Relay
# active_high=True based on your LED test results
pump = OutputDevice(PUMP_PIN, active_high=True, initial_value=False)

def get_moisture_percent():
    """Reads voltage and converts to percentage based on calibration."""
    voltage = chan.voltage
    percentage = ((V_DRY - voltage) / (V_DRY - V_WET)) * 100
    # Constrain between 0-100%
    return max(0, min(100, round(percentage, 1)))

def check_and_water():
    """Checks moisture and triggers pump if necessary."""
    current_moisture = get_moisture_percent()
    print(f"Current Moisture: {current_moisture}%")
    
    if current_moisture < MOISTURE_THRESHOLD:
        print(f"Moisture is below {MOISTURE_THRESHOLD}%. Starting pump for {WATERING_DURATION}s...")
        pump.on()
        time.sleep(WATERING_DURATION)
        pump.off()
        print("Watering complete.")
    else:
        print("Moisture level is sufficient. No watering needed.")

if __name__ == "__main__":
    check_and_water()
