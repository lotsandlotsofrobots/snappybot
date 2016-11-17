from ada_moto_v2 import *
from pyduinoincludes import *
from synapse.PWM import *

motorPower =  50 # (0% - 100%) Power used to drive a motor
turnTime   = 250 # (milliseconds) Delay used by LEFT and RIGHT

# This is how the robot motors are wired
left_front_motor_channel  = 0
right_front_motor_channel = 3
left_back_motor_channel   = 1
right_back_motor_channel  = 2

# startup event initializes the hardware
@setHook(HOOK_STARTUP)
def _startup():    
    setPinDir(0, True)
    i2cInit(False, SCL, SDA)
    ada_moto_init()
    init_adps_9960()
    # TODO initialize the color sensor
    
def FORWARD():
    ada_moto_fwd(left_front_motor_channel, motorPower)
    ada_moto_fwd(right_front_motor_channel, motorPower)    
    ada_moto_fwd(left_back_motor_channel, motorPower)
    ada_moto_fwd(right_back_motor_channel, motorPower)

def BACK():
    ada_moto_rev(left_front_motor_channel, motorPower)
    ada_moto_rev(right_front_motor_channel, motorPower)    
    ada_moto_rev(left_back_motor_channel, motorPower)
    ada_moto_rev(right_back_motor_channel, motorPower)

def STOP():
    ada_moto_stop(left_front_motor_channel)
    ada_moto_stop(right_front_motor_channel)
    ada_moto_stop(left_back_motor_channel)
    ada_moto_stop(right_back_motor_channel)

def LEFT():
    ada_moto_fwd(right_front_motor_channel, motorPower)
    ada_moto_rev(left_front_motor_channel, motorPower)
    ada_moto_fwd(right_back_motor_channel, motorPower)
    ada_moto_rev(left_back_motor_channel, motorPower)
    _delay(turnTime)
    STOP()

def RIGHT():
    ada_moto_rev(right_front_motor_channel, motorPower)
    ada_moto_fwd(left_front_motor_channel, motorPower)
    ada_moto_rev(right_back_motor_channel, motorPower)
    ada_moto_fwd(left_back_motor_channel, motorPower)
    _delay(turnTime)
    STOP()
    
# 0=FrontLeft, 1=FrontRight, 2=BackLeft, 3=BackRight
def testMotor(motor):
    if motor == 0:
        ada_moto_fwd(left_front_motor_channel, motorPower)
    elif motor == 1:
        ada_moto_fwd(right_front_motor_channel, motorPower)
    elif motor == 2:
        ada_moto_fwd(left_back_motor_channel, motorPower)
    elif motor == 3:
        ada_moto_fwd(right_back_motor_channel, motorPower)
    _delay(1000)
    STOP()
    
def _delay(ticksInMs):
    tick = 0
    # blocking pulse of 1ms - the best?  no.  quick and works?  yes!
    while tick < ticksInMs:
        pulsePin(0, -1000, False)
        tick = tick+1
 
def go_forward(msecs):
    FORWARD()
    _delay(msecs)
    STOP()
    
def go_back(msecs):      
    BACK() 
    _delay(msecs)
    STOP()
    
def turn_left(msecs):    
    ada_moto_fwd(right_front_motor_channel, motorPower)
    ada_moto_rev(left_front_motor_channel, motorPower)
    ada_moto_fwd(right_back_motor_channel, motorPower)
    ada_moto_rev(left_back_motor_channel, motorPower)
    _delay(msecs)
    STOP()
    
def turn_right(msecs):
    ada_moto_rev(right_front_motor_channel, motorPower)
    ada_moto_fwd(left_front_motor_channel, motorPower)
    ada_moto_rev(right_back_motor_channel, motorPower)
    ada_moto_fwd(left_back_motor_channel, motorPower)
    _delay(msecs)
    STOP()

def go_til_green():
    FORWARD()
    while getColor() != 'Green':
        continue
    STOP()    
    
def go_til_red():
    FORWARD()
    while getColor() != 'Red':
        continue
    STOP()
    
def go_til_blue():
    FORWARD()
    while getColor() != 'Blue':
        continue
    STOP()