import threading
import HUD
from flask import Flask
from InputExecutable import ControllerExecution
import InputExecutable
from flask_socketio import SocketIO
from flask_cors import CORS
import time

webApp = HUD.HUDweb
webApp.config['SECRET_KEY'] = 'secret!'
CORS(webApp, resources={r"/*": {"origins": "*"}})
controllerSocket = SocketIO(webApp, cors_allowed_origins="*")

# ROVstate = SocketIO(webApp)
# def EmitVideoFeed():
#     while True:
#         controllerSocket.emit('video_feed'), {}
        
def emit_controller_data():
    while True:
        # print(f"Emitting stopped state: {InputExecutable.stopped}")  # Debugging print
        controllerSocket.emit('controllerData', {
            'axis_X': InputExecutable.axis_X,
            'axis_Yaw': InputExecutable.axis_Yaw,
            'axis_Z': InputExecutable.axis_Z
        })
        time.sleep(0.1)
        
def emit_state_data():
    while True:
        controllerSocket.emit('ToggleState', {'stopped': InputExecutable.stopped})
        time.sleep(0.1)  # Small delay for throttling emissions

def EmitAltitudeData():
    while True:
        controllerSocket.emit('AltitudeData', {'altID': InputExecutable.altID})
            

def ThreadCreator(function):
    _thread = threading.Thread(target=function)
    _thread.daemon = True
    _thread.start()
    return _thread

def RunApp(app):
    app.run(host='0.0.0.0', port=5000)
    
if __name__ == '__main__':
    
    controller_thread = threading.Thread(target=ControllerExecution)
    controller_thread.daemon = True
    controller_thread.start()
    
    emit_thread = threading.Thread(target=emit_controller_data)
    emit_thread.daemon = True
    emit_thread.start()
    
    emit_state_thread = threading.Thread(target=emit_state_data)
    emit_state_thread.daemon = True
    emit_state_thread.start()
    
    # # alt_thread = threading.Thread(target=EmitAltitudeData)
    # # alt_thread.daemon = True
    # # alt_thread.start()

    #MAKE HUD VERY LAST THREAD
    flaskThread = threading.Thread(target=RunApp(webApp))
    flaskThread.daemon = True
    flaskThread.start()
    
    while True:
        time.sleep(0.5)
    