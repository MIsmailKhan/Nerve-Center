import cv2
import numpy as np


def rotate(frame , i):
	(h,w) = frame.shape[:2]
	c = (w/2,h/2)
	mat = cv2.getRotationMatrix2D(c,i,1)
	dst = cv2.warpAffine(frame,mat,(w,h))
	return dst

pos = cv2.imread("pos.jpg")
neg = cv2.imread("neg.jpg")
neg=cv2.resize(neg,(640,480))
xpos,ypos,channel = pos.shape
xneg,yneg,channel2=neg.shape
print xpos,ypos,xneg,yneg

mask=np.ones((xneg,yneg))

posrotate=rotate(pos,60)
xrot,yrot,_=posrotate.shape
print xrot,yrot
cv2.imshow('rotated image',posrotate)

#creating the mask
posrotatecopy = posrotate.copy()
posrotatecopy=cv2.cvtColor(posrotatecopy,cv2.COLOR_BGR2GRAY)
ret,maskimage = cv2.threshold(posrotatecopy, 1, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('masked',maskimage)
print maskimage.shape

flag=0
while (not flag):
	y = np.random.random_integers(0,xneg,size=1)
	x = np.random.random_integers(0,yneg,size=1)
	if x+xrot > xneg:
		flag=1
	if y+yrot > yneg:
		flag=1
croppedneg=neg[x:x+xrot,y:y+yrot]

cv2.imshow("cropped negative image",croppedneg)
print croppedneg.shape
#posout = cv2.bitwise_and(croppedneg,croppedneg,mask = maskimage)
cv2.waitKey(0)



