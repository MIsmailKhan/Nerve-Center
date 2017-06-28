import cv2
import cv2.cv as cv

# from time import time

count = 0
boxes = []
startbox = [0,0]
i=0
flag = 0
def on_mouse(event, x, y, flags, params):
    global count
    global i
    global flag
    global startbox

    if event == cv.CV_EVENT_LBUTTONDOWN:

        startbox = [x, y]
        boxes.append(startbox)
        flag = 1

    # if event == cv2.EVENT_MOUSEMOVE:
    
    #     if flag == 1:
    #         movebox = [x+5,y+5]
    #         movebox=tuple(movebox)
    #         startbox=tuple(startbox)
    #         print startbox
    #         print movebox
    #         # cv2.rectangle(img, boxes[i], boxes[i+1], (0, 255, 0), 2)
    #         # import pdb;pdb.set_trace()
    #         # cv2.rectangle(img, startbox, movebox, (0, 255, 0), 2)
    #         # print i

    elif event == cv.CV_EVENT_LBUTTONUP:
        
        endbox = [x, y]
        boxes.append(endbox)
        print boxes
        crop = img[boxes[-2][1]:boxes[-1][1],boxes[-2][0]:boxes[-1][0]]
        # crop = img[boxes[0][1]:boxes[1][1],boxes[0][0]:boxes[1][0]]
        cv2.imshow("crop",crop)
        cv2.imwrite(str(count)+".jpg",crop)
        count +=1
	


cap = cv2.VideoCapture('C:\Users\MohammadIsmail\Desktop\TestVideo\S2.avi')
cv2.namedWindow('real image')
cv.SetMouseCallback('real image', on_mouse, 0)

while(1):
    #img = cv2.imread('pluto.jpg')
    ret,img = cap.read()

    cv2.imshow('real image', img)
    # cv2.imshow('real image', img)
    
    key = cv2.waitKey(50)
    if key ==ord('p'):
        while(cv2.waitKey(50)!=	ord('r')):pass
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
    
