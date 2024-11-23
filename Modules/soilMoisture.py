#!/usr/bin/env python
import ADC0832
import time
import RPi.GPIO as GPIO
import random

# GPIO pins for the RGB LED
RGB_PINS = [5, 6, 13]
THRESHOLD = 2  # Moisture threshold

def init():
	ADC0832.setup()
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	for pin in RGB_PINS:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)

def turn_off_leds():
	for pin in RGB_PINS:
		GPIO.output(pin, GPIO.HIGH)

def loop():
	while True:
		adc_value = ADC0832.getADC(0)
		moisture = 255 - adc_value
		print (f'Analog value: {adc_value:03d}  Moisture: {moisture}')
		
		if moisture >= THRESHOLD:
			turn_off_leds()
			selected_pin = random.choice(RGB_PINS)
			GPIO.output(selected_pin, GPIO.LOW)
			print (f"Moisture threshold reached! LED on GPIO{selected_pin} is ON.")
		else:
			turn_off_leds()
			print ("Moisture below threshold. LEDs are OFF.")
		
		time.sleep(3.5)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
		print ('The end !')
