import numpy as np
import cv2
import math
#from matplotlib import pyplot as plt

initposy=initposx=finalposy=finalposx=flag = 0
crop=[]
framearray=[]
i=0

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
        hist = cv2.calcHist([hsv_crop], [0, 1], None, [180, 256], [0, 180, 0, 256])
        axes = plt.gca()
        axes.set_xlim([100, 200])
        axes.set_ylim([0, 50])
        plt.imshow(hist)
        plt.show()

cap = cv2.VideoCapture('C:\Users\MohammadIsmail\Desktop\TestVideo\Sicario.mkv')
ret, prevframe2 = cap.read()
grayprev2=cv2.cvtColor(prevframe2,cv2.COLOR_BGR2GRAY)
ret,prevframe=cap.read()
grayprev=cv2.cvtColor(prevframe,cv2.COLOR_BGR2GRAY)
mask_diff1 = np.zeros(grayprev.shape,dtype=np.int8)
mask_diff2 = mask_diff1
mask_diff3 = mask_diff2
mask_diff4 = mask_diff3
decay = np.zeros(grayprev.shape)
ret,prev2frame=cap.read()
grayprev2=cv2.cvtColor(prev2frame,cv2.COLOR_BGR2GRAY)
"""
#print prevframe.shape
#cv2.namedWindow('image')
#cv2.setMouseCallback('image', draw_circle,0)


#while (1):
#    cv2.imshow('image', prevframe)
#    if cv2.waitKey(20) & 0xFF == 27:
#        break

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
"""
#print 'b'
while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('Original Video', frame)
    if (ret):
        #masking the image, background subtraction, tracking all movement in the frame
        grayframe=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        diff1=cv2.absdiff(grayframe,grayprev)
        cv2.imshow('first difference',diff1)
        diff2 = cv2.absdiff(grayprev, grayprev2)
        cv2.imshow('second difference', diff2)
        diff=cv2.bitwise_and(diff1,diff2,mask=None)
        cv2.imshow('Difference',diff)

        mask_diff=cv2.inRange(diff,70,255)
        np.put(mask_diff,[1],[255])

        #bettering the object movement , eventually to be used for object tracking
        x=0.5
        decay=mask_diff+(mask_diff+(((1-x)*mask_diff1).astype('uint8')))+(((math.pow(1-x,2))*mask_diff2).astype('uint8'))+(((math.pow(1-x,3))*mask_diff3).astype('uint8'))+(((math.pow(1-x,4))*mask_diff4).astype('uint8'))
        decaykernel=np.ones((7,7),np.uint8)
        decay = cv2.morphologyEx(decay, cv2.MORPH_CLOSE, decaykernel, iterations=3)
        cv2.imshow('decayed', decay)
        diff_colour = cv2.bitwise_and(frame, frame, mask=decay)
        #cv2.imshow('Decayed Mask with colour', diff_colour)



        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([12, 150,0])
        upper = np.array([20,190,200])
        mask_image=cv2.inRange(hsv,lower,upper)
        #cv2.imshow('unrefined',mask_image)
        kernel=np.ones((7,7),np.uint8)
        mask_image=cv2.morphologyEx(mask_image, cv2.MORPH_CLOSE,kernel,iterations=3)
        #cv2.imshow('refined with open',mask_image)
        #mask_image = cv2.morphologyEx(mask_image, cv2.MORPH_CLOSE, (5, 5))
        #cv2.imshow('Refined with both close+open', mask_image)
        res = cv2.bitwise_and(frame, frame, mask=mask_image)


        movingdocketonly=cv2.bitwise_and(decay, decay,mask=mask_image)
        cv2.imshow('Docket only',movingdocketonly)

        object_track, contours, hierarchy = cv2.findContours(movingdocketonly, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        q=cv2.drawContours(res, contours, -1, (0, 255, 0), 3)
        cv2.imshow('Object being tracked',res)

        """
        #meanshift stuff down
        hsv = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1) # meanshift/camshift on backprojection only
        #cv2.imshow('dst',dst)
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)
        x, y, w, h = track_window
        img2 = cv2.rectangle(diff, (x, y), (x + w, y + h), 255, 2)
        #cv2.imshow('img2', img2)
        """
        grayprev2= grayprev
        grayprev= grayframe

        mask_diff1 = mask_diff
        mask_diff2 = mask_diff1
        mask_diff3 = mask_diff2
        mask_diff4 = mask_diff3




        k=cv2.waitKey(20) & 0xFF
        if k==27:
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()