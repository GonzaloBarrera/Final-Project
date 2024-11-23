import os
import time
import RPi.GPIO as GPIO

# GPIO setup
MOTOR_PIN = 19  # GPIO pin for motor control
ONE_WIRE_GPIO = 23  # GPIO pin connected to the DS18B20

def setup_gpio():
    GPIO.setwarnings(False)  # Suppress warnings about channel usage
    GPIO.setmode(GPIO.BCM)   # Use BCM pin numbering
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Ensure motor is off initially

# Read the temperature from the DS18B20 sensor
def read_temperature():
    try:
        base_dir = "/sys/bus/w1/devices/"
        device_folder = [folder for folder in os.listdir(base_dir) if folder.startswith("28-")][0]
        device_file = os.path.join(base_dir, device_folder, "w1_slave")

        with open(device_file, "r") as f:
            lines = f.readlines()

        if "YES" not in lines[0]:
            raise Exception("Sensor not ready")

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

# Control the motor based on the temperature
def control_motor(temperature, threshold):
    if temperature >= threshold:
        GPIO.output(MOTOR_PIN, GPIO.LOW)  # Start motor
        print("Threshold reached! Motor started.")
    else:
        GPIO.output(MOTOR_PIN, GPIO.HIGH)  # Stop motor
        print("Temperature is below threshold. Motor stopped.")

# Main loop
def main():
    setup_gpio()
    try:
        threshold = float(input("Set a threshold temperature (Celsius) between 29 and 32: "))
        if not 29 <= threshold <= 32:
            print("Threshold must be between 29 and 32.")
            return
    except ValueError:
        print("Invalid threshold value.")
        returns

    try:
        while True:
            temperature = read_temperature()
            if temperature is not None:
                print(f"Temperature: {temperature:.2f} Celsius")
                control_motor(temperature, threshold)
            else:
                print("Failed to read temperature. Retrying...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
