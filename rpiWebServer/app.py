import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledYlw = 17
ledGrn = 19
ledBlu = 18

ledYlwSts = 0
ledGrnSts = 0
ledBluSts = 0

GPIO.setup(ledYlw, GPIO.OUT)
GPIO.setup(ledGrn, GPIO.OUT)
GPIO.setup(ledBlu, GPIO.OUT)

GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)
GPIO.output(ledBlu, GPIO.LOW)

@app.route("/")
def index():
    ledBluSts = GPIO.input(ledBlu)
    ledYlwSts = GPIO.input(ledYlw)
    ledGrnSts = GPIO.input(ledGrn)
    templateData = {
        'title': 'GPIO output status',
        'ledBlu': ledBluSts,
        'ledYlw': ledYlwSts,
        'ledGrn': ledGrnSts,
    }
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'ledBlu':
        actuator = ledBlu
    if deviceName == 'ledYlw':
        actuator = ledYlw
    if deviceName == 'ledGrn':
        actuator = ledGrn
    
    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)

    ledBluSts = GPIO.input(ledBlu)
    ledYlwSts = GPIO.input(ledYlw)
    ledGrnSts = GPIO.input(ledGrn)

    templateData = {
        'ledBlu': ledBluSts,
        'ledYlw': ledYlwSts,
        'ledGrn': ledGrnSts, 
    }
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)    