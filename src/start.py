from .Rover import * 
from .roverClean import *


def mainStart(serial=None, connection=None):
    if serial != None:
        print(serial)
        rover = Rover(roverSerial=serial,connection=connection)
        cleanArea(rover=rover)
        #sweep(rover=rover)

if __name__ == '__main__':
    pass
else:
    mainStart()