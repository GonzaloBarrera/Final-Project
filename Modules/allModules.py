#!/usr/bin/env python
import os
import time
import RPi.GPIO as GPIO
import ADC0832
import random

# GPIO pins for DS18B20
MOTOR_PIN = 19          # GPIO pin for motor control
ONE_WIRE_GPIO = 23      # GPIO pin connected to the DS18B20

# GPIO pins for soil moisture RGB LED
RGB_PINS = [5, 6, 13]
SOIL_MOISTURE_THRESHOLD = 2       # Moisture threshold

# GPIO pins for photoresistor LEDs
LED_PIN_ON = 21
LED_PIN_OFF = 20
PHOTORESISTOR_THRESHOLD = 128     # Light threshold

def setup_gpio():
    """Initialize GPIO settings."""
    # DS18B20 setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_PIN, GPIO.OUT)
    GPIO.output(MOTOR_PIN, GPIO.HIGH)    # Ensure motor is off initially
    
    # Soil moisture LED setup
    for pin in RGB_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)      # Turn off all RGB LEDs
    
    # Photoresistor LED setup
    GPIO.setup(LED_PIN_ON, GPIO.OUT)
    GPIO.setup(LED_PIN_OFF, GPIO.OUT)
    
    # ADC setup
    ADC0832.setup()

def turn_off_rgb_leds():
    """Turn off all RGB LEDs."""
    for pin in RGB_PINS:
        GPIO.output(pin, GPIO.HIGH)

def read_temperature():
    """Read temperature from DS18B20 sensor."""
    try:
        base_dir = "/sys/bus/w1/devices/"
        device_folders = [folder for folder in os.listdir(base_dir) if folder.startswith("28-")]
        if not device_folders:
            raise Exception("No DS18B20 sensor detected")
        device_folder = device_folders[0]
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

def control_motor(temperature, threshold):
    """Control motor based on temperature."""
    if temperature >= threshold:
        GPIO.output(MOTOR_PIN, GPIO.LOW)        # Start motor
    else:
        GPIO.output(MOTOR_PIN, GPIO.HIGH)       # Stop motor

def read_soil_moisture():
    """Read soil moisture from ADC."""
    adc_value = ADC0832.getADC(0)
    moisture = 255 - adc_value
    return adc_value, moisture

def handle_soil_moisture(moisture):
    """Control RGB LED based on soil moisture."""
    if moisture >= SOIL_MOISTURE_THRESHOLD:
        turn_off_rgb_leds()
        selected_pin = random.choice(RGB_PINS)
        GPIO.output(selected_pin, GPIO.LOW)
    else:
        turn_off_rgb_leds()

def read_light_intensity():
    """Read light intensity from photoresistor via ADC."""
    return ADC0832.getADC(1)

def handle_light_intensity(adc_value):
    """Control LEDs based on light intensity."""
    if adc_value < PHOTORESISTOR_THRESHOLD:
        print('Dark')
        GPIO.output(LED_PIN_ON, GPIO.HIGH)
        GPIO.output(LED_PIN_OFF, GPIO.LOW)
    else:
        print('Light')
        GPIO.output(LED_PIN_ON, GPIO.LOW)
        GPIO.output(LED_PIN_OFF, GPIO.HIGH)

def main():
    setup_gpio()
    try:
        threshold = float(input("Set a threshold temperature (Celsius) between 29 and 32: "))
        if not 29 <= threshold <= 32:
            print("Threshold must be between 29 and 32.")
            return
    except ValueError:
        print("Invalid threshold value.")
        return

    try:
        while True:
            # Temperature handling
            temperature = read_temperature()
            if temperature is not None:
                print(f"Temperature: {temperature:.2f} Celsius")
                control_motor(temperature, threshold)
            else:
                print("Failed to read temperature. Retrying...")

            # Soil moisture handling
            adc_value, moisture = read_soil_moisture()
            print(f"Soil Moisture - Analog value: {adc_value:03d}, Moisture: {moisture}")
            handle_soil_moisture(moisture)

            # Light intensity handling
            light_adc_value = read_light_intensity()
            print(f"Light Intensity - ADC value: {light_adc_value}")
            handle_light_intensity(light_adc_value)

            time.sleep(1)  # Adjust sleep time as necessary
    except KeyboardInterrupt:
        print("Exiting...")
        ADC0832.destroy()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
