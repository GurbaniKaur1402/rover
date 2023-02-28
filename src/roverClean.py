from .util import keyboard_shutdown
import time
import math

length = 45
breadth = 30

#True = edge detected

def coverForwardArea(rover, spd):
    rover.moveF(speed=spd)

def coverBackwardArea(rover, spd):
    rover.moveB(speed=spd)

def MoveForward(rover, spd, d):
    rover.moveF_L(speed=spd,d=d)

def MoveBackward(rover, spd, d):
    rover.moveB_L(speed=spd,d=d)

def changeDirection(rover, angle):
    rover.changeYaw(angle=angle,speed=0.02)

def sweep(rover):
    print("Sweeeping")
    try:
        while(rover.ul_front_edge.checkDriveOk() == True):
                        
            if (rover.ul_back_edge.checkDriveOk() == True):
                changeLane(rover=rover)
                print("Change Lane function called")

            else:
                coverBackwardArea(rover,spd=2)
                print("Moving Back")

        else:
            coverForwardArea(rover,spd=2)
            print("Moving Fwd")

    except KeyboardInterrupt:
        keyboard_shutdown()  

def changeLane(rover):
    print("Changing Lane")
    H = math.sqrt(((length/2)**2)+(breadth**2))
    theta = math.atan((breadth)/(length/2))

    try:
        while(rover.ul_back_edge.checkDriveOk() == True):
            
            MoveForward(rover,spd=2, d=int((length/2)))
            changeDirection(rover, theta)
    
            if (rover.ul_front_edge.checkDriveOk() == True):
            # Lane End
                print("Lane End")
                changeDirection(rover, -theta)
                MoveBackward(rover,spd=2, d=int((length/2)))
                #check drone status
                #call dock function()
                break

            else:
                MoveForward(rover,spd=2, d=int((H)))
                changeDirection(rover, (-theta))
                MoveBackward(rover,spd=2, d=int((3*length)/2))

    except KeyboardInterrupt:
        keyboard_shutdown()  

def cleanArea(rover):
    print('check drone status')
    rover.workingStatus = True
    rover.setupAndArm()
    rover.changeVehicleMode('GUIDED')
    time.sleep(2)
    
    try:
        if ((rover.ul_back_edge.checkDriveOk() == False)): # (rover.ul_front_edge.checkDriveOk() == False)):
            
            MoveForward(rover,spd=2, d=int((length)))
            print("Undocking")
            #wait till drone takeoff
            coverBackwardArea(rover,spd=2)
            time.sleep(1)

            if (rover.ul_back_edge.checkDriveOk() == True):
                changeDirection(rover, 90)
                print("Orienting to corner")
                time.sleep(1)
                
                if (rover.ul_back_edge.checkDriveOk() == True):
                    print("Sweep function called")
                    sweep(rover=rover)
                    time.sleep(1)
            
                else:
                    coverBackwardArea(rover,spd=2)
                    print("Going to Top-Right corner")  
                    time.sleep(1)
            else:
                coverBackwardArea(rover,spd=2)
                print("Going to Top edge")
                time.sleep(1)
        
        else:
            
            if(rover.ul_back_edge.checkDriveOk() == False):
                coverForwardArea(rover,spd=2)
                print("Caution Forward")
                time.sleep(1)
                
            elif(rover.ul_front_edge.checkDriveOk() == False):
                coverBackwardArea(rover,spd=2)
                print("Caution Backward")
                time.sleep(1)
                

    except KeyboardInterrupt:
        keyboard_shutdown()