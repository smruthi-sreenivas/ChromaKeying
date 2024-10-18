import cv2
import matplotlib.pyplot as plt
import numpy as np

#(59.73649343232439, 165.82318675042833, 70.80639634494575)
rect_start = None
rect_end = None
start = False
color = None
tolerance = None

lower_green, upper_green = np.array([0,0,0]),np.array([0,0,0])

smooth = None
cast = None

# mouse callback function to select rectangular patch
def drawRect(event,x,y,flags,param):
    global rect_start, rect_end, start, color

    if event == cv2.EVENT_LBUTTONDOWN:
        rect_start = (x,y)
        start = True #started selecting the rectangular patch

    elif event == cv2.EVENT_LBUTTONUP:
        rect_end = (x,y)
        start = False
        #extract the rectangular patch and find its average
        if rect_start and rect_end:
            x1,y1 = rect_start
            x2,y2 = rect_end
            if x1>x2 :
                x1,x2 = x2,x1
            if y1>y2:
                y1,y2 = y2,y1
            patch = frame_resized[y1:y2,x1:x2]
            color = cv2.mean(patch)[:3]
           # print(f"color BGR: {color}")

def colorTolerance(*args):
    global tolerance, color,lower_green, upper_green
    tolerance = args[0]

def apply_chroma_key(frame,background):
    global color,lower_green,upper_green,tolerance,smooth,cast
    lower_green = np.array([color[0] - tolerance, color[1] - tolerance, color[2] - tolerance])
    upper_green = np.array([color[0] + tolerance, color[1] + tolerance, color[2] + tolerance])
    #create a mask where color is found.
    ''''image pixel falls in the range of the lower and upper colour thresholds. If it does fall in this range, 
    the mask will be allowed to be displayed and if not it will block it out and turn the pixel black.'''
    mask = cv2.inRange(frame,lower_green,upper_green)
    #invert the mask for the foreground
    mask_inv = cv2.bitwise_not(mask)
    #Extract the foreground not matching the green color
    foreground = cv2.bitwise_and(frame,frame,mask = mask_inv)
    #resize background to match frame_resized
    bg_resized = cv2.resize(background, (640, 480))
    #get the background on the mask(green) area
    background = cv2.bitwise_and(bg_resized,bg_resized,mask = mask)
    #combine foreground and background
    #smoothen the foreground
    foreground = cv2.GaussianBlur(foreground,(smooth,smooth),0)
    if cast is not None and (cast > 0):
        foreground = reduceGreenCast(foreground,cast)
    window_name = 'foreground'
    cv2.imshow(window_name,foreground)

    frame_new = cv2.add(foreground, background)
    window_name = 'merged'
    cv2.imshow(window_name, frame_new)



def smoothenFrame(*args):
    global smooth
    smooth = args[0]
    if smooth % 2 != 1:
        smooth = smooth + 1

def colorCastRemoval(*args):
    global cast
    cast = args[0]
    cast = cast/100.0

def reduceGreenCast(image,cast):
    b,g,r = cv2.split(image)
    g = np.clip(g*(1-cast),0,255) #higher values of cast means more suppression of green
    g = g.astype(np.uint8)
    image = cv2.merge((b,g,r))
    return image

#create a video reader object
cap = cv2.VideoCapture("greenscreen-demo.mp4")
if (cap.isOpened() == False):
    print("Error opening video file.")
print(cap.get(3)) #width
print(cap.get(4)) #height

background = cv2.imread('background1.png')
#read frames until video is completed
window_name = 'Green Screen Effect'
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name,drawRect)
cv2.createTrackbar("Color Tolerance",window_name,50,100,colorTolerance)
cv2.createTrackbar("Softness Slider",window_name,5,10,smoothenFrame)
cv2.createTrackbar("ColorCast Removal",window_name,0,30,colorCastRemoval)
while (cap.isOpened()):
    ret, frame = cap.read()
    if color is None:
        cv2.putText(frame, "Click on a color to replace",
                    (100, 180), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 3)
        if rect_start and rect_end :
            cv2.rectangle(frame_resized,rect_start,rect_end,(0,0,0),2)
    if ret == True:

        frame_resized = cv2.resize(frame, (640, 480))


        if color is not None:
             apply_chroma_key(frame_resized,background)


        cv2.imshow(window_name, frame_resized)

        cv2.waitKey(25) #wait for 25ms before moving on to next frame. This will slow down video.
    else:
        break


cv2.destroyAllWindows()




