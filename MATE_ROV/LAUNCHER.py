import threading
import HUD
import InputExecutable
from flask import Flask

webApp = HUD.HUDweb
# inputReader = INPUTCONTROLLER.InputReader

def RunApp(app):
    app.run()


if __name__ == '__main__':
    flaskThread = threading.Thread(target=RunApp(webApp))
    # inputThread = threading.Thread(target=RunApp(inputReader))

    flaskThread.start()
    # inputThread.start()