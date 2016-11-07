from ada_moto_v2 import *
from pyduinoincludes import *
from synapse.PWM import *

motorPower = 50
left_front_motor_channel = None
right_front_motor_channel = None
left_back_motor_channel = None
right_back_motor_channel = None




def motor_controller_startup(left_front_motor, right_front_motor, left_back_motor, right_back_motor, reverse_all):
    global left_front_motor_channel, right_front_motor_channel, left_back_motor_channel, right_back_motor_channel, motorPower
    left_front_motor_channel = left_front_motor
    right_front_motor_channel = right_front_motor
    left_back_motor_channel = left_back_motor
    right_back_motor_channel = right_back_motor
    setPinDir(0, True)
    i2cInit(False, SCL, SDA)
    ada_moto_init()
    init_adps_9960()
    

def testMotor(motor):
    if motor == 0:
        ada_moto_fwd(left_front_motor_channel, motorPower)
    elif motor == 1:
        ada_moto_fwd(right_front_motor_channel, motorPower)
    elif motor == 2:
        ada_moto_fwd(left_back_motor_channel, motorPower)
    elif motor == 3:
        ada_moto_fwd(right_back_motor_channel, motorPower)
    delay(1000)
    stop()
    
def delay(ticksInMs):
    tick = 0
    # blocking pulse of 1ms - the best?  no.  quick and works?  yes!
    while tick < ticksInMs:
        pulsePin(0, -1000, False)
        tick = tick+1
    
def forward(seconds):
    go()
    delay(seconds*1000)
    stop()
    
def go():
    ada_moto_fwd(left_front_motor_channel, motorPower)
    ada_moto_fwd(right_front_motor_channel, motorPower)    
    ada_moto_fwd(left_back_motor_channel, motorPower)
    ada_moto_fwd(right_back_motor_channel, motorPower)    


def stop():
    ada_moto_stop(left_front_motor_channel)
    ada_moto_stop(right_front_motor_channel)
    ada_moto_stop(left_back_motor_channel)
    ada_moto_stop(right_back_motor_channel)
    
    
def turn_left():
    ada_moto_fwd(right_front_motor_channel, motorPower)
    ada_moto_rev(left_front_motor_channel, motorPower)
    ada_moto_fwd(right_back_motor_channel, motorPower)
    ada_moto_rev(left_back_motor_channel, motorPower)
    delay(250)
    stop()
    
    
def turn_right():
    ada_moto_rev(right_front_motor_channel, motorPower)
    ada_moto_fwd(left_front_motor_channel, motorPower)
    ada_moto_rev(right_back_motor_channel, motorPower)
    ada_moto_fwd(left_back_motor_channel, motorPower)
    delay(250)
    stop()

def go_til_green():
    go()
    while getColor() != 'Green':
        continue
    stop()
    
    
def go_til_red():
    go()
    while getColor() != 'Red':
        continue
    stop()
    
def go_til_blue():
    go()
    while getColor() != 'Blue':
        continue
    stop()