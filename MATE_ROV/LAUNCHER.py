import threading
import HUD
from flask import Flask, request
from InputExecutable import ControllerExecution
from flask_socketio import SocketIO
from flask_cors import CORS
import time
import asyncio

webApp = HUD.HUDweb
webApp.config['SECRET_KEY'] = 'secret!'
CORS(webApp, resources={r"/*": {"origins": "*"}})
controllerSocket = SocketIO(webApp, cors_allowed_origins="*")

controlApp = HUD.ControlApp
controlApp.config['SECRET_KEY'] = 'secret!'
CORS(controlApp, resources={r"/*": {"origins": "*"}})
inputSocket = SocketIO(controlApp, cors_allowed_origins="*")

peers = {}

# class VideoReciever(VideoStreamTrack):
#     def __init__(self) -> None:
#         super().__init__()
    
#     async def recv(self):
#         frame = await super().recv()
#         img = frame.to
        

# ROVstate = SocketIO(webApp)

# def EmitVideoFeed():
#     while True:
#         controllerSocket.emit('video_feed'), {}
        
def emit_controller_data():
    while True:
        # print(f"Emitting stopped state: {InputExecutable.stopped}")  # Debugging print
        controllerSocket.emit('controllerData', {
            'axis_X': ControllerExecution.axis_X,
            'axis_Yaw': ControllerExecution.axis_Yaw,
            'axis_Z': ControllerExecution.axis_Z
        })
        time.sleep(0.1)
        
def emit_state_data():
    while True:
        controllerSocket.emit('ToggleState', {'stopped': ControllerExecution.stopped})
        time.sleep(0.1)  # Small delay for throttling emissions

def EmitAltitudeData():
    while True:
        controllerSocket.emit('AltitudeData', {'altID': ControllerExecution.altID})
            

def ThreadCreator(function):
    _thread = threading.Thread(target=function)
    _thread.daemon = True
    _thread.start()
    return _thread

def RunApp(app, _port):
    app.run(host='0.0.0.0', port= _port)
    

    
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
    
    inputThread = threading.Thread(target=RunApp(controlApp, 5005))
    inputThread.daemon = True
    inputSocket.start()

    flaskThread = threading.Thread(target=RunApp(webApp, 5000))
    flaskThread.daemon = True
    flaskThread.start()
    
    while True:
        time.sleep(0.5)
    