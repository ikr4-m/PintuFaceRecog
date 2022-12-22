from decouple import config
from serial import Serial

arduino = Serial(port=config('ARDUINO_PORT_SERIAL'), baudrate=9600, timeout=.1)
arduino.write(bytes("1", 'utf-8'))