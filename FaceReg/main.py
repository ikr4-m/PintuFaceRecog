from decouple import config
from serial import Serial

arduino = Serial(port=config('ARDUINO_PORT_SERIAL'), baudrate=9600, timeout=.1)
arduino.write(bytes("0", 'utf-8'))