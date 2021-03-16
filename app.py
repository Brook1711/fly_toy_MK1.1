from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app)

import RPi.GPIO as GPIO

PIN_left = 14
PIN_right = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_left, GPIO.OUT)
GPIO.setup(PIN_right, GPIO.OUT)

p_left = GPIO.PWM(PIN_left, 50)
p_right = GPIO.PWM(PIN_right, 50)

p_left.start(0)
p_right.start(0)


values = {
    'v': 0,
    'h': 0,
}

@app.route('/')
def index():
    return render_template('index.html', **values)

@socketio.on('value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    v = float(values['v'])
    h = float(values['h'])
    l = 0 + (v + h*0.5) * 1
    r = 0 + (v - h*0.5) * 1
    p_left.ChangeDutyCycle(float(l))
    p_right.ChangeDutyCycle(float(r))
    print('l : ', l, '   r : ', r)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')