# GPIO enums to be used in example scripts, mapped to Pyduino IO numbers as supported by the SNAP core firmware
D0 = 16
D1 = 17
D2 = 20
D3 = 5
D4 = 23
D5 = 6
D6 = 7
D7 = 12
D8 = 0
D9 = 19
D10 = 21
D11 = 37
D12 = 4
D13 = 22
SDA = 9
SCL = 8

# Analog channels
A0 = 0
A1 = 1
A2 = 4
A3 = 5
A4 = 6
A5 = 7
SENSE_5V = 2

# User-controlled LED
LED_PIN = 18

# List of pin assignments that can be iterated over in Pyduino-pin-order (i.e. D0 is 16, D1 is 17, etc...)
DIGITAL_TO_IO_LIST = (16, 17, 20, 5, 23, 6, 7, 12, 0, 19, 21, 37, 4, 22, 9, 8)
ANALOG_LIST = (A0, A1, A2, A3, A4, A5)