import numpy as np
import cv2



initposy=initposx=finalposy=finalposx=flag = 0
crop=[]

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global initposy,initposx,finalposy,finalposx
    global crop

    if event == cv2.EVENT_LBUTTONDOWN:
        initposx=x
        initposy=y
        print initposx
        print initposy
        flag=1
    elif event==cv2.EVENT_LBUTTONUP:
        finalposx=x
        finalposy=y
        print "final"
        print finalposx,initposx
        print finalposy,initposy
        crop=prevframe[initposy:finalposy,initposx:finalposx]
        cv2.imshow("cropped image",crop)
        cv2.imwrite("cropped.jpg", crop)
        hsv_crop=cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        print hsv_crop

cap = cv2.VideoCapture('C:\Users\MohammadIsmail\Desktop\TestVideo\Docket.mp4')
ret, prevframe = cap.read()
print prevframe.shape
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle,0)


while (1):
    cv2.imshow('image', prevframe)
    if cv2.waitKey(20) & 0xFF == 27:
        break


#hsv_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
#hist = cv2.calcHist([hsv_crop], [0, 1], None, [180, 256], [0, 180, 0, 256])
#print hist

if(ret):
    # setup initial location of window
    r, h, c, w = 250, 90, 400, 125
    track_window = (c, r, w, h)

    roi = prevframe[r:r + h, c:c + w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

#print 'b'

while (cap.isOpened()):
    ret, frame = cap.read()
    if (ret):
        #lineframe=cv2.line(frame,(0,0),(854,480),(255,0,0),5)
        #cv2.imshow('test',lineframe)
        diff = cv2.absdiff(frame, prevframe)
        cv2.imshow('frame0',frame)
        cv2.imshow('frame1',diff)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 140, 150])
        upper = np.array([30,170,180])
        mask_image=cv2.inRange(hsv,lower,upper)
        res = cv2.bitwise_and(frame, frame, mask=mask_image)
        cv2.imshow('colour detection',res)

        #meanshift stuff down
        hsv = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1) # meanshift/camshift on backprojection only
        #cv2.imshow('dst',dst)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        x, y, w, h = track_window
        img2 = cv2.rectangle(diff, (x, y), (x + w, y + h), 255, 2)
        #cv2.imshow('img2', img2)

        prevframe=frame

        k=cv2.waitKey(20) & 0xFF
        if k==27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


