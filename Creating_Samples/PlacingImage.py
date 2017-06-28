import cv2
import numpy as np

# original image
# -1 loads as-is so if it will be 3 or 4 channel as the original
def rotate(frame , i):
	(h,w) = frame.shape[:2]
	c = (w/2,h/2)
	mat = cv2.getRotationMatrix2D(c,i,1)
	dst = cv2.warpAffine(frame,mat,(w,h))
	return dst

pos = cv2.imread("pos.jpg")
neg = cv2.imread("neg.jpg")
neg=cv2.resize(neg,(640,480))
posrotate=rotate(pos,60)

grayed=cv2.cvtColor(posrotate, cv2.COLOR_BGR2GRAY)
cv2.imshow("grayed",grayed)
masked=cv2.threshold(grayed,1,255,cv2.THRESH_BINARY)
cv2.imshow('masked image',masked)
extracted=cv2.bitwise_and(posrotate,posrotate,mask=masked)
cv2.imshow("only rotated",extracted)

cv2.imshow('rotated pic',posrotate)
cv2.waitKey(0)