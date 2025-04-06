import pygame
from flask_socketio import SocketIO
from flask_cors import CORS
import time
pygame.init()
pygame.joystick.init()
stopped = False
controllers = {}
cameras = {}

def ControllerCreator(controllerID, controllerName):
    if pygame.joystick.get_count()>0:
        controllerName = pygame.joystick.Joystick(controllerID)
        controllerName.init()

        try:
            controllerPrint = controllerName.get_instance_id()
            print(f"{controllerName} found at: {controllerPrint}")
            print(controllerName.get_name())
            controllers[controllerName] = controllerID

            return controllerName
        except:
            print("exception found")
    else:
        print ("no stick found")

def DebugController(controller):
    if not controller:
        print(f"{controller} not found")
    else:
        print(f"{controller} intialized")

driver = ControllerCreator(1, "driverID")
operator = ControllerCreator(0, "operatorID")



DebugController(driver)
DebugController(operator)

#For camera
inputCamera = 0

# #Driver Inputs
axis_X = 0.0
axis_Z = 0.0
axis_Yaw = 0.0
axis_Y = 0.0

#servo test binds
firstGear = False
secondGear = False
thirdGear = False
neutral = False
arming = False

def ToggleStop():
    # wasStopped = False
    global stopped
    stopped = not stopped    
    
def AltitudeControl():
    if descend:
        ascend = False
    elif ascend:
        descend = False
#Main function
def ControllerExecution():
    global inputCamera
    
    def CameraSwitchIndex(val):
        print(f"key int: {val}")
        return val
    
    global axis_X, axis_Yaw, axis_Z, axis_Y
    global neutral, firstGear, secondGear, thirdGear, arming
    screen = pygame.display.set_mode((1, 1))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #   EMERGENCY STOP
                if event.key == pygame.K_DELETE:
                    run = False
                # DISABLE
                if event.key == pygame.K_SPACE:
                    ToggleStop()
                    print(stopped)
                if event.key == pygame.K_RSHIFT:
                    ToggleStop()
                    print(stopped)

                #For Cameras
                if event.key == pygame.K_o:
                   inputCamera = CameraSwitchIndex(event.key)
                    
                elif event.key == pygame.K_i:
                   inputCamera = CameraSwitchIndex(event.key)            

        if stopped:
            continue
        if not stopped:
            if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION, pygame.JOYHATMOTION]:
                joystick_id = event.instance_id
                # print(f"Joystick Event: {event}")
                
                time.sleep(0.1)
                
                if joystick_id == driver.get_instance_id():
                    
                    if event.type == pygame.JOYHATMOTION:
                        print(f"DPAD: {event}")
                    #press events
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 6:
                            neutral = True
                        elif event.button == 7:
                            firstGear = True
                        elif event.button == 8:
                            secondGear = True
                        elif event.button == 9:
                            thirdGear = True
                        elif event.button == 10:
                            arming = True
                    #release events
                    if event.type == pygame.JOYBUTTONUP:
                         if event.button == 6:
                            neutral = False
                         elif event.button == 7:
                            firstGear = False
                         elif event.button == 8:
                            secondGear = False
                         elif event.button == 9:
                            thirdGear = False   
                         elif event.button == 10:
                             arming = False
                    
                
                if joystick_id == driver.get_instance_id():
                    if event.type == pygame.JOYAXISMOTION:
                            #Axis Commands
                            if event.axis == 0:
                                axis_X = event.value
                            elif event.axis == 1:
                                axis_Z = event.value
                            elif event.axis == 2:
                                axis_Yaw = event.value
                            elif event.axis == 3:
                                axis_Y = event.value
                           
    pygame.quit()    

