import RPi.GPIO as GPIO

import time

from flask import Flask, jsonify

 

app = Flask(__name__)

 

# GPIO pin numbers (change these according to your setup)

TRIGGER_PIN = 11

ECHO_PIN = 12

 

# Configure GPIO pins

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIGGER_PIN, GPIO.OUT)

GPIO.setup(ECHO_PIN, GPIO.IN)

 

def measure_distance():

    # Set trigger pin to HIGH for 10 microseconds

    GPIO.output(TRIGGER_PIN, GPIO.HIGH)

    time.sleep(0.00001)

    GPIO.output(TRIGGER_PIN, GPIO.LOW)

 

    # Measure the duration of the pulse from the echo pin

    while GPIO.input(ECHO_PIN) == GPIO.LOW:

        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:

        pulse_end = time.time()

 

    # Calculate distance based on the pulse duration

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150  # Speed of sound (343 m/s) divided by 2

    distance = round(distance, 2)  # Round to two decimal places

    return distance

 

@app.route('/distance', methods=['GET'])

def get_distance():
    while True:
        distance = measure_distance()

        return jsonify({'distance': distance})
        time.sleep(1)

 

if __name__ == '__main__':

    try:

        app.run(host='0.0.0.0', port=5000)  # Run the Flask app

    except KeyboardInterrupt:

        GPIO.cleanup()
