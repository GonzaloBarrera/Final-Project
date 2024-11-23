#!/usr/bin/env python
import ADC0832
import time
import RPi.GPIO as GPIO

# Constants for conversion
ADC_MAX_VALUE = 255  # Maximum ADC value
VREF = 3.3           # Reference voltage in volts
LED_PIN_ON = 21
LED_PIN_OFF = 20

def init():
    ADC0832.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN_ON, GPIO.OUT)
    GPIO.setup(LED_PIN_OFF, GPIO.OUT)

def loop():
    while True:
        adc_value = ADC0832.getADC(1)
        print (adc_value)
        if adc_value < 128:
            print('dark')
            GPIO.output(LED_PIN_ON, GPIO.HIGH)
            GPIO.output(LED_PIN_OFF, GPIO.LOW)
        else:
            print('light')
            GPIO.output(LED_PIN_ON, GPIO.LOW)
            GPIO.output(LED_PIN_OFF, GPIO.HIGH)
        time.sleep(0.2)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt: 
        ADC0832.destroy()
        GPIO.cleanup()
        print ('The end !')
