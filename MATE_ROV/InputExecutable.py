import pygame

pygame.init()
pygame.joystick.init()
stopped = False
controllers = {}


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

# #Driver Inputs
axis_X = 0
axis_Z = 0
axis_Yaw = 0
#for altitude
altID = 0
# -1, 0, 1
#  D, N, A

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
    global axis_X, axis_Z, axis_Yaw
    screen = pygame.display.set_mode((1, 1))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
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

        if stopped:
            continue
        if not stopped:
            if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION, pygame.JOYHATMOTION]:
                joystick_id = event.instance_id
                print(f"Joystick Event: {event}")

                if joystick_id == driver.get_instance_id():
                    if event.type == pygame.JOYAXISMOTION:
                            #Axis Commands
                            if event.axis == 0:
                                axis_X = event.value
                            elif event.axis == 1:
                                axis_Z = event.value
                            elif event.axis == 2:
                                axis_Yaw = event.value
                                                        
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        altID = -1
                    elif event.button == 2:
                        altID = 1
                    else: altID = 0
                           
    pygame.quit()    

