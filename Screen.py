from flask import Flask, jsonify,request
from PIL import Image,ImageGrab
import time
import cv2
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

####Settings####
FramesPerSecond = 8 # max fps is framegroups * 8
XRes = 16*35   # 16*20 #
YRes = 9*35 # 9*20

KeyInput = True

CompressedColors = False
FrameGroups = 1 #keep to low amounts such as 3 

FrameSkip = 0

FrameStart = 0
VideoStreaming = True
VideoPath = r"mp4 file path here"
####Settings####

LastFrame = []
FrameCount = 1

ServerList = {}

cap = cv2.VideoCapture(VideoPath)

cap.set(cv2.CAP_PROP_POS_FRAMES,FrameStart)

def RGBToCompHex(rgb):
    return f"{(rgb[0] >> 4):X}{(rgb[1]  >> 4):X}{(rgb[2] >> 4):X}"

def EncodeFrame(FirstTime,ServerID,SkipFrame):     
    global LastFrame,FrameCount

    if VideoStreaming and SkipFrame == "1":
        ServerList[ServerID] += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES,ServerList[ServerID]);
    
    if FirstTime == "1":
        #Refresh the clients screen (doesnt compress it)
        LastFrame = []
    
    
    lastpixel = ""
    lastenumerate,lastDuplicate = 0,0
    number,DuplicateNumber = 1,1
    
    WasDuplicate = False
    WasRepetitive = False

    if not VideoStreaming:
        pic = ImageGrab.grab().resize((XRes,YRes),Image.Resampling.BILINEAR)
    else:
        playing, frame = cap.read()
        if not playing:
            #video ended, go to 1st
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            ServerList[ServerID] = 0
            _, frame = cap.read()
        
        pic = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((XRes,YRes),Image.Resampling.BILINEAR)
    
    if CompressedColors:
        CurrentFrame = [RGBToCompHex(pixel) for pixel in pic.getdata()]
    else:
        CurrentFrame = ["%02x%02x%02x" % pixel for pixel in pic.getdata()]


    #removes duplicates
    LastFrame2 = [*CurrentFrame]

    FrameLen = len(LastFrame)
    
    for i,v in enumerate(CurrentFrame):
        #Removes non changed colors
        if FrameLen > i and v == LastFrame[i]:
            if WasDuplicate:
                DuplicateNumber += 1
                CurrentFrame[lastDuplicate] = DuplicateNumber
                CurrentFrame[i] = '' 
            else:
                CurrentFrame[i] = 1
                lastDuplicate = i
                DuplicateNumber = 1
            WasDuplicate = True
            continue
        else:
            WasDuplicate = False
        
        #Removes color repetition
        if lastpixel == v:
            if WasRepetitive:
                number += 1
                CurrentFrame[lastenumerate] = number
                CurrentFrame[i] = ''
            else:
                CurrentFrame[i] = 1.1
                lastenumerate = i
                number = 1.1
            WasRepetitive = True
        else:
            lastpixel = v
            WasRepetitive = False
    
    FrameCount += 1
    if FrameCount < FrameSkip:
        LastFrame = []
    else:
        LastFrame = LastFrame2
    
    return tuple(filter(None, CurrentFrame))

@app.route('/',methods=['POST'])
def ReturnFrame():
    global ServerList
    Method = request.headers["R"]
    
    ServerID = request.headers["I"]
    SkipFrame = request.headers["F"]

    if not ServerID in ServerList:
        ServerList[ServerID] = FrameStart
    
    #Prints all the servers that its keeping track of
    print(ServerList)
    
    Frames = []
    
    RealWait = 0
    for _ in range(FrameGroups):
        #makes the frames "flow" smoother
        start = time.time()
        
        Frames.append(EncodeFrame(Method,ServerID,SkipFrame))
        
        RealWait = max(0,1/FramesPerSecond - (time.time()-start))
        time.sleep(RealWait)
        print(RealWait)
    
    return jsonify(Fr=Frames,F=FramesPerSecond,X=XRes, Y=YRes, G=FrameGroups)

def StartApi(Port):
    print(str(XRes) + "x" + str(YRes) + "     Port:" + str(Port))
    Server = WSGIServer(('127.0.0.1', Port), app)
    Server.serve_forever()

StartApi(1241)