import cv2 as cv
import numpy as np

#variable with HSV value of measured pixel
px_hsv = []

#default variable of HSV range values, 
#nothing special just anything to define new variable
min_h = 10
min_s = 10
min_v = 10
max_h = 10
max_s = 10
max_v = 10

#trackbars need some function to operate correctly, 
#so I generated empty one
def nothing(_):
    pass

#mouse function operate all events from mouse:
#- Move of cursor
#- LMB Double click
def mouse(event,x,y,flags,param):
    global px_hsv, min_h, min_s, min_v, max_h, max_s, max_v
    if event == cv.EVENT_MOUSEMOVE:
        #showing converted HSV value of pixel under cursor
        px = frame[x,y]
        px_array = np.uint8([[px]])
        px_hsv = cv.cvtColor(px_array,cv.COLOR_BGR2HSV)
    elif event == cv.EVENT_LBUTTONDBLCLK:
        #get x,y position of cursor and convert its value to HSV
        px = frame[x,y]
        px_array = np.uint8([[px]])
        px_hsv = cv.cvtColor(px_array,cv.COLOR_BGR2HSV)
        #set minimum and maximum values of range, of the selected colour,
        #represented by pixel I double clicked on
        #range is set to -20/+20. Is it enough?
        min_h = (px_hsv[0][0][0]-20 if px_hsv[0][0][0]-20 > 0 else 0)
        min_s = (px_hsv[0][0][1]-40 if px_hsv[0][0][1]-20 > 0 else 0)
        min_v = (px_hsv[0][0][2]-40 if px_hsv[0][0][2]-20 > 0 else 0)
        max_h = (px_hsv[0][0][0]+20 if px_hsv[0][0][0]+20 < 180 else 180)
        max_s = (px_hsv[0][0][1]+20 if px_hsv[0][0][1]+20 < 255 else 255)
        max_v = (px_hsv[0][0][2]+40 if px_hsv[0][0][2]+20 < 255 else 255)

#start recording
cap = cv.VideoCapture(0)

#create new window, video with main view directly
#from the camera and attach mouse operations to it
cv.namedWindow('video')
cv.setMouseCallback("video",mouse)

while True:
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of color in HSV

    cv.createTrackbar("H1", "video", min_h, 180, nothing)
    cv.createTrackbar("S1", "video", min_s, 255, nothing)
    cv.createTrackbar("V1", "video", min_v, 255, nothing)
    cv.createTrackbar("H2", "video", max_h, 180, nothing)
    cv.createTrackbar("S2", "video", max_s, 255, nothing)
    cv.createTrackbar("V2", "video", max_v, 255, nothing)

    h1 = cv.getTrackbarPos('H1', 'video')
    s1 = cv.getTrackbarPos('S1', 'video')
    v1 = cv.getTrackbarPos('V1', 'video')
    h2 = cv.getTrackbarPos('H2', 'video')
    s2 = cv.getTrackbarPos('S2', 'video')
    v2 = cv.getTrackbarPos('V2', 'video')

    lower = np.array([h1,s1,v1])
    upper = np.array([h2,s2,v2])

    # Threshold the HSV video to get only colour in defined range
    mask = cv.inRange(hsv, lower, upper)

    #text with HSV value on the main screen
    pixel_hsv = " ".join(str(values) for values in px_hsv)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(frame, "px HSV: "+pixel_hsv, (10, 260), 
               font, 1, (255, 255, 255), 1, cv.LINE_AA)

    # Bitwise-AND mask and original video
    cv.imshow('video',frame)
    cv.imshow('mask',mask)

    #click ESC to exit the program
    key = cv.waitKey(5) & 0xFF
    if key == 27:
        break
cv.destroyAllWindows()