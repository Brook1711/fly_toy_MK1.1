from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
app = Flask(__name__)
socketio = SocketIO(app)

servo_pin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
p = GPIO.PWM(servo_pin, 50)
p.start(0)


values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('index.html', **values)

@socketio.on('value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    p.ChangeDutyCycle(float(values['myRange']))
    print(values)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')