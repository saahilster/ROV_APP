import threading
import HUD
from flask import Flask, request
from InputExecutable import ControllerExecution
import InputExecutable
from flask_socketio import SocketIO
from flask_cors import CORS
import time

# Initialize Flask app
webApp = HUD.HUDweb
webApp.config['SECRET_KEY'] = 'secret!'
CORS(webApp, resources={r"/*": {"origins": "*"}})

# Initialize Flask-SocketIO
controllerSocket = SocketIO(webApp, cors_allowed_origins="*", async_mode='gevent')

@controllerSocket.on('client_message')
def handle_message(msg):
    print(f'Got message: {msg}')
    controllerSocket.emit('server_response', f'Server got: {msg}')

# # Thread function to emit camera data
# def CameraCyclerEmitter():
#     while True:
#         try:
#             controllerSocket.emit('Cycle Data', InputExecutable.inputCamera)
#             time.sleep(0.1)  # Small delay to prevent flooding
#         except Exception as e:
#             print(f"Error in camera emitter: {e}")
#             time.sleep(0.5)  # Wait before retrying

# Thread function to emit controller data
def emit_controller_data():
    while True:
        controllerSocket.emit('controllerData', {
            'axis_X': InputExecutable.axis_X,
            'axis_Yaw': InputExecutable.axis_Yaw,
            'axis_Z': InputExecutable.axis_Z,
            'depth': InputExecutable.axis_Y,
            'neutral': InputExecutable.neutral,
            'first': InputExecutable.firstGear,
            'second': InputExecutable.secondGear,
            'third': InputExecutable.thirdGear,
            'arm': InputExecutable.arming,
            'up': InputExecutable.up,
            'down': InputExecutable.down,
            'left': InputExecutable.left,
            'right': InputExecutable.right,
            'A' : InputExecutable.arm
        })
        time.sleep(0.1)
         
# Thread function to emit state data
# def emit_state_data():
#     while True:
#         controllerSocket.emit('ToggleState', {'stopped': InputExecutable.stopped})
#         time.sleep(0.1)

# Thread function to emit altitude data
# def EmitAltitudeData():
#     while True:
#         controllerSocket.emit('AltitudeData', {'altID': InputExecutable.altID})
#         time.sleep(0.1)

# Helper function to create and start a thread
def ThreadCreator(function):
    _thread = threading.Thread(target=function)
    _thread.daemon = True
    _thread.start()
    return _thread

# Function to start the Flask-SocketIO server
def RunApp(app, socketio):
    socketio.run(app, host='192.168.2.1', port=5000)

if __name__ == '__main__':

    # Start the controller execution thread
    ThreadCreator(ControllerExecution)

    # Start background emission threads
    ThreadCreator(emit_controller_data)
    # ThreadCreator(emit_state_data)
    # ThreadCreator(CameraCyclerEmitter)

    # Start Flask-SocketIO server in a separate thread
    flaskThread = threading.Thread(target=RunApp, args=(webApp, controllerSocket))
    flaskThread.daemon = True
    flaskThread.start()

    while True:
        time.sleep(0.25)
