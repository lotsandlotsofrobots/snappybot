from pyduinoincludes import *

AGAIN_4X=1
PGAIN_4X=2
LED_DRIVE_100MA=0
GGAIN_4X=2
GWTIME_2_8MS=1

APDS9960_CONTROL="\x8F"
APDS9960_ENABLE="\x80"

APDS9960_CDATAL="\x94"
APDS9960_CDATAH="\x95"
APDS9960_RDATAL="\x96"
APDS9960_RDATAH="\x97"
APDS9960_GDATAL="\x98"
APDS9960_GDATAH="\x99"
APDS9960_BDATAL="\x9A"
APDS9960_BDATAH="\x9B"
APDS9960_CONFIG1="\x8D"
APDS9960_CONFIG2="\x90"
APDS9960_CONFIG3="\x9F"
APDS9960_AILTL="\x84"
APDS9960_AILTH="\x85"
APDS9960_AIHTL="\x86"
APDS9960_AIHTH="\x87"
APDS9960_PERS="\x8C"
APDS9960_GCONF1="\xA2"
APDS9960_GCONF2="\xA3"
APDS9960_GCONF3="\xAA"
APDS9960_GCONF4="\xAB"
APDS9960_GOFFSET_U="\xA4"
APDS9960_GOFFSET_D="\xA5"
APDS9960_GOFFSET_L="\xA7"
APDS9960_GOFFSET_R="\xA9"
APDS9960_GPULSE="\xA6"
APDS9960_PPULSE="\x8E"
APDS9960_GPENTH="\xA0"
APDS9960_GEXTH="\xA1"
APDS9960_PILT="\x89"
APDS9960_PIHT="\x8B"
APDS9960_POFFSET_DL="\x9E"
APDS9960_POFFSET_UR="\x9D"
APDS9960_WTIME="\x83"

DEFAULT_ATIME=0xDB #219
DEFAULT_WTIME=0xF6 #246
DEFAULT_PROX_PULSE=0x87  #0x87
DEFAULT_POFFSET_UR=0x00
DEFAULT_POFFSET_DL=0x00
DEFAULT_CONFIG1=0x60 #0x60
DEFAULT_LDRIVE=LED_DRIVE_100MA
DEFAULT_PGAIN=PGAIN_4X
DEFAULT_AGAIN=AGAIN_4X
DEFAULT_PILT=0x00
DEFAULT_PIHT=0x32 #50
DEFAULT_AILT=0xffff
DEFAULT_AIHT=0x00
DEFAULT_PERS=0x11
DEFAULT_CONFIG2=0x01
DEFAULT_CONFIG3=0x00
DEFAULT_GPENTH=0x40
DEFAULT_GEXTH=0x30
DEFAULT_GCONF1=0x40
DEFAULT_GGAIN=GGAIN_4X
DEFAULT_GLDRIVE=LED_DRIVE_100MA
DEFAULT_GWTIME=GWTIME_2_8MS
DEFAULT_GOFFSET=0x00
DEFAULT_GPULSE=0xC9
DEFAULT_GCONF3=0x00
DEFAULT_GIEN=0x00
DEFAULT_PROX_PPULSE=0x87

POWER=0
AMBIENT_LIGHT=1
ALL=7

WRITE_ADDR="\x72"
READ_ADDR="\x73"


def getMode():
    val = readDataByte(APDS9960_ENABLE)
    return val


def setMode(mode, enable):
    val = getMode()
    enable = enable & 0x01
    if ( mode >= 0 and mode <=6 ):
        if enable is True:
            val |= (1 << mode)
        else:
            val |= ~(1 << mode)
    elif ( mode == ALL ):
        if enable is True:
            val = "\x7F"
        else:
            val = "\x00"
    writeDataByte(APDS9960_ENABLE, val)


def enablePower():
    setMode(POWER, 1)


def readDataByte(register):
    i2cWrite(WRITE_ADDR + register, 10, False)
    i2cResult = getI2cResult()
    if i2cResult != 1:
        print "ERROR:  couldn't write, i2cResult was ", str(i2cResult)
        return None
        
    byte = i2cRead(READ_ADDR, 1, 10, False)
    #print "readDataByte returned: ", str(byte)
    i2cResult = getI2cResult()
    #print "readDataByte i2cResult returned: ", str(i2cResult)
    if i2cResult != 1:
        print "ERROR:  couldn't read, i2cResult ", str(i2cResult)
        return None
    #print "readDataByte about to return ", ord(byte)
    return ord(byte)

def writeDataByte(register, byte):
    if byte is None:
        print "YOU FORGOT BYTE DUMMY"
    
    #register = chr(register)
    byte = chr(byte)
    byteString = register + str(byte)
    if errno() != 0:
        print "Register: " + ord(register) + " byte: " + int(byte)
    i2cWrite(WRITE_ADDR + byteString, 10, False)
    if getI2cResult() != 1:
        return None
    #else:
    #    print "write: OK"
    return 0

def setAmbientLightGain(gain):
    rva = readDataByte(APDS9960_CONTROL)
        
    if rva is None:
        return -1
    #else:
    #    print "ambientLightGain: ", str(rva)
        
    gain &= 0x3
    #print "after int/ord, val is ", str(rva)
    rva |= gain
    #print "after or equals, val is ", str(rva)
    #print "about to write ", rva
    
    rva = writeDataByte(APDS9960_CONTROL, rva)
    
    if rva is None:
        return -1
    
    #re read back
    val = readDataByte(APDS9960_CONTROL)
    if rva is None:
        return -1
    else:
        print "post write ambient light gain ", str(val)

def setAmbientLightIntEnable(enable):
    val = readDataByte(APDS9960_ENABLE)
    
    if val is None:
        print "setAmbientLightIntEnable:  READ FAIL"
        return None
    
    enable &= 0x1
    enable = enable << 4
    val &= 0xEF
    val |= enable
    rva = writeDataByte(APDS9960_ENABLE, val)
    if rva is None:
        print "setAmbientLightGain: WRITE FAIL"
        return None


def setLEDDrive(drive):
    val = readDataByte(APDS9960_CONTROL)
    drive &= 0x3
    drive = drive << 6
    val &= 0x3F
    val |= drive
    writeDataByte(APDS9960_CONTROL, val)

def setProxIntLowThresh(threshold):
    writeDataByte(APDS9960_PILT, threshold)

def setProxIntHighThresh(threshold):
    writeDataByte(APDS9960_PIHT, threshold)

def setLightIntLowThreshold(threshold):
    low = threshold & 0x00FF
    high = (threshold & 0xFF00) >> 8
    writeDataByte(APDS9960_AILTL, low)
    writeDataByte(APDS9960_AILTH, high)

def setLightIntHighThreshold(threshold):
    low = 0x00FF
    high = (threshold & 0xFF00) >> 8
    writeDataByte(APDS9960_AIHTL, low)
    writeDataByte(APDS9960_AIHTH, high)


def setGestureEnterThresh(threshold):
    writeDataByte(APDS9960_GPENTH, threshold)

def setGestureExitThresh(threshold):
    writeDataByte(APDS9960_GEXTH, threshold)

def setGestureGain(gain):
    val = readDataByte(APDS9960_GCONF2)
    gain &= 0x3
    gain = gain << 5
    val &= 0x9F
    val |= gain
    writeDataByte(APDS9960_GCONF2, val)

def setGestureLEDDrive(drive):
    val = readDataByte(APDS9960_GCONF2)
    drive &= 0x3
    drive = drive << 3
    drive &= 0xE7
    val |= drive
    writeDataByte(APDS9960_GCONF2, val)

def setGestureWaitTime(time):
    val = readDataByte(APDS9960_GCONF2)
    time &= 0x7
    val &= 0xF8
    val |= time
    writeDataByte(APDS9960_GCONF2, val)
    
def setGestureIntEnable(enable):
    val = readDataByte(APDS9960_GCONF4)
    enable &= 0x01
    enable = enable << 1
    val &= 0xFD
    val |= enable
    writeDataByte(APDS9960_GCONF4, val)
    
def setProximityGain(gain):
    val = readDataByte(APDS9960_CONTROL)
    gain &= 0x3
    gain = gain << 2;
    val &= 0xF3
    val |= gain
    writeDataByte(APDS9960_CONTROL, val)


def readAmbientLight():
    val_l = readDataByte(APDS9960_CDATAL)
    val_h = readDataByte(APDS9960_CDATAH)
    val = val_l + (val_h<<8)
    return val

def readRed():
    val_l = readDataByte(APDS9960_RDATAL)
    val_h = readDataByte(APDS9960_RDATAH)
    val = val_l + (val_h<<8)
    return val

def readGreen():
    val_l = int(readDataByte(APDS9960_GDATAL))
    val_h = int(readDataByte(APDS9960_GDATAH))
    val = val_l + (val_h<<8)
    return val

def readBlue():
    val_l = readDataByte(APDS9960_BDATAL)
    val_h = readDataByte(APDS9960_BDATAH)
    val = val_l + (val_h<<8)
    return val

def getColor():
    ambient = readAmbientLight()
    red = readRed()
    green = readGreen()
    blue = readBlue()
    twoThirdsRed = red/2
    twoThirdsGreen = green/2
    twoThirdsBlue = blue/3*2
    oneThirdAmbient = ambient/2
    tenPercentAmbient = ambient/10
    if twoThirdsRed > green and twoThirdsRed > blue and red > oneThirdAmbient:
        return "Red"
    elif twoThirdsGreen > red and twoThirdsGreen > blue and green > oneThirdAmbient:
        return "Green"
    elif twoThirdsBlue > red and twoThirdsBlue > green and blue > oneThirdAmbient:
        return "Blue"
    redMinusGreen = red - green
    redMinusBlue = red - blue
    greenMinusBlue = green - blue
    if redMinusGreen < 0:
        redMinusGreen *= -1
    if redMinusBlue < 0:
        redMinusBlue *= -1
    if greenMinusBlue < 0:
        greenMinusBlue *= -1
    if redMinusGreen < tenPercentAmbient and redMinusBlue < tenPercentAmbient \
        and greenMinusBlue < tenPercentAmbient:
        return "White or black"
    else:
        return None
    
    

def init():
    setMode(ALL, 0)
    writeDataByte(APDS9960_WTIME, DEFAULT_WTIME)
    writeDataByte(APDS9960_PPULSE, DEFAULT_PROX_PPULSE)
    writeDataByte(APDS9960_POFFSET_UR, DEFAULT_POFFSET_UR)
    writeDataByte(APDS9960_POFFSET_DL, DEFAULT_POFFSET_DL)
    writeDataByte(APDS9960_CONFIG1, DEFAULT_CONFIG1)
    setLEDDrive(DEFAULT_LDRIVE)
    setProximityGain(DEFAULT_PGAIN)
    setAmbientLightGain(DEFAULT_AGAIN)
    setProxIntLowThresh(DEFAULT_PILT)
    setProxIntHighThresh(DEFAULT_PIHT)
    setLightIntLowThreshold(DEFAULT_AILT)
    setLightIntHighThreshold(DEFAULT_AIHT)
    writeDataByte(APDS9960_PERS, DEFAULT_PERS)
    writeDataByte(APDS9960_CONFIG2, DEFAULT_CONFIG2)
    writeDataByte(APDS9960_CONFIG3, DEFAULT_CONFIG3)
    setGestureEnterThresh(DEFAULT_GPENTH)
    setGestureExitThresh(DEFAULT_GEXTH)
    writeDataByte(APDS9960_GCONF1, DEFAULT_GCONF1)
    setGestureGain(DEFAULT_GGAIN)
    setGestureLEDDrive(DEFAULT_GLDRIVE)
    setGestureWaitTime(DEFAULT_GWTIME)
    writeDataByte(APDS9960_GOFFSET_U, DEFAULT_GOFFSET)
    writeDataByte(APDS9960_GOFFSET_D, DEFAULT_GOFFSET)
    writeDataByte(APDS9960_GOFFSET_L, DEFAULT_GOFFSET)
    writeDataByte(APDS9960_GOFFSET_R, DEFAULT_GOFFSET)
    writeDataByte(APDS9960_GPULSE, DEFAULT_GPULSE)
    writeDataByte(APDS9960_GCONF3, DEFAULT_GCONF3)
    setGestureIntEnable(DEFAULT_GIEN)
    setPinDir(D8, True)
    setPinDir(D10, True)
    writePin(D8, False)
    writePin(D10, False)
    
def headlights_on():
    writePin(D8, True)
    writePin(D10, True)

def headlights_off():
    writePin(D8, False)
    writePin(D10, False)

def init_adps_9960():
    i2cInit(False, SCL, SDA)
    init()
    rva = setAmbientLightGain(DEFAULT_AGAIN)
    if rva == -1:
        print "set ambient light gain FAILED!"
    setAmbientLightIntEnable(0)
    if rva == -1:
        print "set ambient light int enable FAILED"
    enablePower()
    setMode(AMBIENT_LIGHT, 1)

def test():
    i2cInit(False, SCL, SDA)
    
    i2cWrite("\x72\x92", 10, False)
    er = errno()
    print "FIRST Errno was:  ", er
    i2cresult = getI2cResult()
    print "i2c result was ", i2cresult
    
    val = i2cRead("\x73", 1, 10, False)
    er = errno()
    print "SECOND errno was: ", er
    i2cresult = getI2cResult()
    print "i2c result was ", i2cresult
    
    print "Val was: ", str(ord(val))




