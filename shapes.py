import cv2
import numpy as np
import imutils

circ_buff = [(0.0,0.0)] * 10
circ_buff_ite = 0

def update_buff(x,y):
    circ_buff[circ_buff_ite]=(x,y)
    circ_buff_ite = circ_buff_ite+1
    circ_buff_ite


def nothing(x):
    # any operation
    pass



cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

appear = False

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_red = np.array([36, 25, 25])
    upper_red = np.array([70, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cnts = imutils.grab_contours(contours)

    for (cnt,cnt1) in zip(contours,contours):
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        #print(approx)

        M = cv2.moments(cnt1)
        cX=0
        cY=0
        if(M["m00"]>0.001):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        #print(M)

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            if (M["m00"] > 0.001 and len(approx)>3):
                centre = (cX,cY)
                cv2.circle(frame, centre, 7, (255, 255, 255), -1)

                appear = True


    cv2.rectangle(frame, (500,300), (650,400), (200,200,200), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()