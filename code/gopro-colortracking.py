# OpenCV - grab image/show image
import cv2
import numpy as np

vid=cv2.VideoCapture('/home/pi/Documents/opencv/golf/golfgopro240.mp4')
vid.set(1,325)

# objection detection
objectDetector=cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=16)


while True:
    ret,frame=vid.read()

    # filter for white objects
    hsl=cv2.cvtColor(frame,cv2.COLOR_BGR2HLS)
    Lchannel=hsl[:,:,1]
    mask = cv2.inRange(Lchannel, 240, 255)

    # filter for moving objects
    #mask2=objectDetector.apply(mask)
    # clean up the mask, closer to 255, the more white
    #_,mask2=cv2.threshold(mask2,254,255,cv2.THRESH_BINARY)
    #cv2.imshow('mask2',mask)

    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # sort the contours to get biggest one first (biggest area)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)

    # step through each contour in the array of contours
    for cnt in contours:
        area=cv2.contourArea(cnt)
        # bounding rectangle of individual contour
        (x,y,w,h)=cv2.boundingRect(cnt)
        # area of 50 would be 7x7 pixels
        if area>=300:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

    cv2.imshow('FGmask1',mask)
    cv2.moveWindow('FGmask1',0,500)

    
    cv2.imshow('golf',frame)
    cv2.moveWindow('golf',0,0)
      
    if cv2.waitKey(2000)==ord('q'):
        break

vid.release()
cv2.destroyAllWindows()