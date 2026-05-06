from gpiozero import OutputDevice
from time import sleep

# GPIO 17 corresponds to Pin 11 on the header
PUMP_PIN = 17

# --- TROUBLESHOOTING LOGIC ---
# Most 1-channel 5V relay modules are "Active Low".
# If your relay has a power LED that stays on but the "Status" LED never lights up,
# try changing active_high to True.
IS_ACTIVE_HIGH = True 

pump = OutputDevice(PUMP_PIN, active_high=IS_ACTIVE_HIGH, initial_value=False)

def test_relay():
    try:
        print(f"--- Relay Diagnostic Mode ---")
        print(f"Using GPIO: {PUMP_PIN} (Pin 11)")
        print(f"Logic Type: {'Active High' if IS_ACTIVE_HIGH else 'Active Low'}")
        
        # We will cycle 3 times to make the 'click' easier to hear
        for i in range(1, 4):
            print(f"\nCycle {i}:")
            print("Action: ON (Relay should click, Status LED should light)")
            pump.on()
            sleep(3)
            
            print("Action: OFF (Relay should click, Status LED should dim)")
            pump.off()
            sleep(3)
            
        print("\nDiagnostic complete.")
        
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")

if __name__ == "__main__":
    test_relay()
