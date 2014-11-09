#
# This is a small example of the python drone API - an ultra minimal GCS
# Usage:
# * mavproxy.py --master=/dev/ttyACM0,115200
# * module load api
# * api start microgcs.py
#
from droneapi.lib import VehicleMode, Location
from pymavlink import mavutil
from Tkinter import *
import cv2
import time

# The tkinter root object
global root

# First get an instance of the API endpoint
api = local_connect()
# get our vehicle - when running with mavproxy it only knows about one vehicle (for now)
v = api.get_vehicles()[0]



def getframe():
    
    cap= cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imshow("Webcam",frame)
    cv2.imwrite("img" + str(time.time()) + ".jpg", frame)
    cap.release()
def setMode(mode):
    # Now change the vehicle into auto mode
    v.mode = VehicleMode(mode)

    # Always call flush to guarantee that previous writes to the vehicle have taken place
    v.flush()

def updateGUI(label, value):
    label['text'] = value

def addObserverAndInit(name, cb):
    """We go ahead and call our observer once at startup to get an initial value"""
    cb(name)
    v.add_attribute_observer(name, cb)

def gotomypoint():
    cmds = v.commands
    setMode("GUIDED")
    pointlatitude=25.1755658#25.175427
    pointlongitude=121.4503905#121.450349
    altitude = 15  # in meters
    dest = Location(pointlatitude, pointlongitude, altitude, is_relative=True)
    print "Going to: %s" % dest

    cmds.goto(dest)
    v.flush()
    time.sleep(2)

def showalt():
    v.flush()
    print v.location
    
def refreshtext(label, value):
    label.configure(text=value)
    
root = Tk()
root.wm_title("microGCS - the worlds crummiest GCS")
frame = Frame(root)
frame.pack()

locationLabel = Label(frame, text = "No location", width=60)
locationLabel.pack()
attitudeLabel = Label(frame, text = "No Att", width=60)
attitudeLabel.pack()
modeLabel = Label(frame, text = "mode")
modeLabel.pack()

addObserverAndInit('attitude', lambda attr: updateGUI(attitudeLabel, v.attitude))
addObserverAndInit('location', lambda attr: updateGUI(locationLabel, v.location))
addObserverAndInit('mode', lambda attr: updateGUI(modeLabel, v.mode))

Button(frame, text = "AltHold", command = lambda : setMode("ALT_HOLD")).pack()
Button(frame, text = "Land", command = lambda : setMode("LAND")).pack()
Button(frame, text = "Guided", command = lambda : setMode("GUIDED")).pack()
Button(frame, text = "FlyToTarget", command = lambda : gotomypoint()).pack()

Button(frame, text = "Refresh!!", command = lambda : refreshtext(modeLabel, v.mode)).pack()
Button(frame, text = "showGPSonCMD!!", command = lambda : showalt() ).pack()

Button(frame, text = "webcamView", command = lambda : getframe()).pack()


root.mainloop()
