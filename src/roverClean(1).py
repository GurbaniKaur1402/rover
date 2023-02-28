from .util import keyboard_shutdown
import time
import math

length = 45
breadth = 30

#True = edge detected

def moveF(rover, spd):
    rover.moveForward(speed=spd)

def moveB(rover, spd):
    rover.moveBackward(speed=spd)

def moveF_L(rover, spd, d):
    rover.moveForward_L(speed=spd,d=d)

def moveB_L(rover, spd, d):
    rover.moveBackward_L(speed=spd,d=d)

def changeDirection(rover, angle):
    rover.changeYaw(angle=angle,speed=0.02)


def changeLane(rover):
    
    print("Changing Lane")
    H = math.sqrt(((length/2)**2)+(breadth**2))
    theta = math.atan((breadth)/(length/2))

    try:
        while(True):
            
            moveF_L(rover,spd=2, d=int((length/2)))
            changeDirection(rover, theta)
    
            # Lane End
            if (rover.ul_front_edge.checkDriveOk() == True):
                print("Lane End")
                changeDirection(rover, -theta)
                moveB_L(rover,spd=2, d=int((length/2)))
                
                while (rover.ul_front_edge.checkDriveOk() == False):
                    moveF(rover=rover)
                
                if (rover.ul_front_edge.checkDriveOk() == True):
        
                    while (rover.ul_front_edge.checkDriveOk() == False):
                        moveB(rover=rover)
        
                    if (rover.ul_back_edge.checkDriveOk() == True):
                        dock(rover=rover)
            
            else:
                moveF_L(rover,spd=2, d=int((H)))
                changeDirection(rover, (-theta))
                moveB_L(rover,spd=2, d=int((3*length)/2))
                break

    except KeyboardInterrupt:
        keyboard_shutdown()


def sweep(rover):
    print("Sweeeping")
    try:
        while(True):
            #at start index
            while (rover.ul_back_edge.checkDriveOk() == False):
                    moveB(rover=rover)

            moveF(rover=rover)
            
            if(rover.ul_front_edge.checkDriveOk() == True):
                while (rover.ul_back_edge.checkDriveOk() == False):
                    moveB(rover=rover)
                if (rover.ul_back_edge.checkDriveOk() == True):
                    changeLane(rover=rover)
#End how?

    except KeyboardInterrupt:
        keyboard_shutdown()  
  

def cleanArea(rover):
    
    print('check drone status')
    rover.workingStatus = True
    rover.setupAndArm()
    rover.changeVehicleMode('GUIDED')
    time.sleep(2)
    
    try:
        moveF_L(rover,spd=2, d=int((length)))
        print("Undocking")
        #wait(5)
        #wait till drone takeoff
        while(True):
            moveB(rover,spd=2)
            time.sleep(1)

            if (rover.ul_back_edge.checkDriveOk() == True):
                changeDirection(rover, 90)
                print("Orienting to corner")
                time.sleep(1)

            moveB(rover,spd=2)            
            if (rover.ul_back_edge.checkDriveOk() == True):
                print("Corner Detected")
                print("Sweep function called")
                sweep(rover=rover)
                break                
        # dock()
    
    except KeyboardInterrupt:
        keyboard_shutdown()

def dock(rover):
    print("Docking")

