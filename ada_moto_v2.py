"""SNAPpy driver for Adafruit Motor Shield v2
   This shield consists of 2 TB6612FNG dual H-bridge chips driven by a PCA9685 PWM controller.
   Note: motor connectors labelled M1-M4 are indexed as channels 0-3
"""

from PCA9685 import *
from apds_9960_rgb_gesture_sensor import *

# Map H-bridge inputs (IN1, IN2, PWM) to PCA9685 channels
ADA_MOTO_PWM_MAP = (
    (10, 9, 8),
    (11, 12, 13),
    (4, 3, 2),
    (5, 6, 7)
)

# H-bridge input indices
HB_IN1 = 0
HB_IN2 = 1
HB_PWM = 2



def ada_moto_init():
    """Initialize motor shield; assumes i2cinit() already invoked"""
    PCA9685_init()
    
def ada_moto_fwd(chan, duty):
    """Drive forward (CW) with 0-100% duty cycle"""
    m = ADA_MOTO_PWM_MAP[chan]
    PCA9685_logic_chan(m[HB_IN1], True)
    PCA9685_logic_chan(m[HB_IN2], False)
    PCA9685_duty_chan(m[HB_PWM], duty * 41)

def ada_moto_rev(chan, duty):
    """Drive reverse (CCW) with 0-100% duty cycle"""
    m = ADA_MOTO_PWM_MAP[chan]
    PCA9685_logic_chan(m[HB_IN1], False)
    PCA9685_logic_chan(m[HB_IN2], True)
    PCA9685_duty_chan(m[HB_PWM], duty * 41)

def ada_moto_brake(chan):
    """Brake - short motor terminals"""
    m = ADA_MOTO_PWM_MAP[chan]
    PCA9685_logic_chan(m[HB_IN1], True)
    PCA9685_logic_chan(m[HB_IN2], True)
    PCA9685_logic_chan(m[HB_PWM], True)
    
def ada_moto_stop(chan):
    """Stop - coast, high impedance to motor terminals"""
    m = ADA_MOTO_PWM_MAP[chan]
    PCA9685_logic_chan(m[HB_IN1], False)
    PCA9685_logic_chan(m[HB_IN2], False)
    PCA9685_logic_chan(m[HB_PWM], True)