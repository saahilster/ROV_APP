import pygame
import sys

pygame.init()

pygame.joystick.init()

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

driver = ControllerCreator(0, "driverID")
operator = ControllerCreator(1, "operatorID")

DebugController(driver)
DebugController(operator)

run = True
while run:
    for event in pygame.event.get():
        print(event)

# def InputReader():
#     while True:
#         for event in pygame.event.get():
#             if event == pygame.QUIT():
#                 pygame.quit()
#                 sys.exit()
#             # if event.type == pygame.JOYAXISMOTION:
#             #     print(f"Axis: {event.axis}, joystick: {event.value}")


pygame.quit()