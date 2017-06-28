import cv2
import numpy as np


def rotate(frame , i):
	(h,w) = frame.shape[:2]
	c = (w/2,h/2)
	mat = cv2.getRotationMatrix2D(c,i,1)
	dst = cv2.warpAffine(frame,mat,(w,h))
	return dst


pos = cv2.imread("pos.jpg")
cv2.imshow("pos",pos)
neg = cv2.imread("neg.jpg")
neg=cv2.resize(neg,(640,480))
hpos,wpos,channel = pos.shape
hneg,wneg,channel2=neg.shape
mask=np.ones((hneg,wneg))
posrotate=rotate(pos,60)
print neg.shape
# posrotate=cv2.bitwise_not(mask)
# posrotate=255-posrotate
# print posrotate
cv2.imshow("numpy",posrotate)
cv2.waitKey(0)
rotx,roty,_=posrotate.shape
print rotx,roty
cv2.imshow('rotated image',posrotate)
posrotatecopy = posrotate.copy()
posrotatecopy=cv2.cvtColor(posrotatecopy,cv2.COLOR_BGR2GRAY)
ret,maskimage = cv2.threshold(posrotatecopy, 1, 255, cv2.THRESH_BINARY)

# cv2.imshow('masked',maskimage)
maskimage=cv2.bitwise_not(maskimage)
cv2.imshow('masked',maskimage)
print maskimage.shape
cv2.waitKey(0)
# cv2.imshow('masked image',maskimage2)
flag=0
while (not flag):
	y = np.random.random_integers(0,wneg,size=1)
	x = np.random.random_integers(0,hneg,size=1)
	if x+rotx > hneg:
		flag=1
	if y+roty > wneg:
		flag=1
croppedneg=neg[x:x+rotx,y:y+roty]
print "hello",croppedneg.shape
croppedneg.shape
posout = cv2.bitwise_and(croppedneg,croppedneg,mask = maskimage)
#cv2.imshow("posout",posout)
cv2.waitKey(0)
#neg[x:x+rotx,y:y+roty]=posout



