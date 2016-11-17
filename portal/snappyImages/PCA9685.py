# (c) Copyright, 2016, Synapse Wireless Inc.
"""Definitions and functions for the NXP PCA9685 12-bit Fm+ 16-ch I2C LED / PWM Driver"""

# I2C address
PCA9685_ADDR = 0xC0  # 0x80 + [A5:A0 pins] -- default here assumes A5 pulled high
PCA9685_ADDR_WR = "%c" % PCA9685_ADDR
PCA9685_ADDR_RD = "%c" % (PCA9685_ADDR + 1)

PCA9685_REG_MODE1 = '\x00'
PCA9685_REG_MODE2 = '\x01'
PCA9685_SUBADR1   = '\x02'
PCA9685_SUBADR2   = '\x03'
PCA9685_SUBADR3   = '\x04'
PCA9685_ALLCALLADR= '\x05'
PCA9685_PWM_BASE  = '\x06'  # Begin 64-byte block: [ON_L | ON_H | OFF_L | OFF_H] * 16
                            # These are waveform ON/OFF counts in a running 12-bit timer.
PCA9685_PWM_ALL   = '\xFA'  # Single 4-byte block (per above) to load ALL the above registers at once
PCA9685_PRESCALE  = '\xFE'
PCA9685_TESTMODE  = '\xFF'

def PCA9685_init():
    """Initialize and exit sleep mode. Enable auto-increment of addressing"""
    i2cWrite(PCA9685_ADDR_WR + PCA9685_REG_MODE1 + "\x20", 1, False)

def PCA9685_sleep():
    """Enter sleep mode"""
    i2cWrite(PCA9685_ADDR_WR + PCA9685_REG_MODE1 + "\x30", 1, False)

def PCA9685_pwm_chan(chan, on, off):
    """Set PWM parameters for selected channel (0-15)"""
    i2cWrite(PCA9685_ADDR_WR + chr(6 + (chan << 2)) + chr(on & 0xff) + chr(on >> 8) + chr(off & 0xff) + chr(off >> 8), 1, False)
    
def PCA9685_pwm_all(on, off):
    """Set PWM parameters for all channels"""
    i2cWrite(PCA9685_ADDR_WR + PCA9685_PWM_ALL + chr(on & 0xff) + chr(on >> 8) + chr(off & 0xff) + chr(off >> 8), 1, False)
    
def PCA9685_logic_chan(chan, is_set):
    """Set logic level output on selected channel"""
    val = "\x00\x10\x00\x00" if is_set else "\x00\x00\x00\x10"
    i2cWrite(PCA9685_ADDR_WR + chr(6 + (chan << 2)) + val, 1, False)
    
def PCA9685_duty_chan(chan, duty):
    """Set PWM duty cycle (n/4096) for selected channel (0-15)"""
    if duty <= 0:
        PCA9685_logic_chan(chan, False)
    elif duty < 4096:
        # Turn on at count=0, off at 'duty' count
        i2cWrite(PCA9685_ADDR_WR + chr(6 + (chan << 2)) + "\x00\x00" + chr(duty & 0xff) + chr(duty >> 8), 1, False)
    else:
        PCA9685_logic_chan(chan, True)