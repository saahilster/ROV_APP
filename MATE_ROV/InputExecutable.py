import pygame
import sys
import time

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
# if driver:
#     axis_X = driver.get_axis(0)
#     axis_Z = driver.get_axis(1)
#     axis_Yaw = driver.get_axis(2)
#     descend = driver.get_button(0)
#     ascend = driver.get_button(2)

def ToggleStop():
    # wasStopped = False
    global stopped
    stopped = not stopped             

#Main function
def ControllerExecution():
    screen = pygame.display.set_mode((1, 1))
    run = True
    while run:
        for event in pygame.event.get():
            #disable robot
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
            print("Code stopped")
        if not stopped:
            if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION, pygame.JOYHATMOTION]:
                joystick_id = event.instance_id

                if joystick_id == driver.get_instance_id():
                    if event.type == pygame.JOYAXISMOTION:
                            #Axis Commands
                            if event.axis == 0:
                                axis_X = event.value
                            elif event.axis == 1:
                                axis_Z = event.value
                            elif event.axis == 2:
                                Yaw = event.value
                                
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        print("Descending")
                    elif event.button == 2:
                        print("Ascending")
                           
    pygame.quit()

ControllerExecution()        


