import cv2
import numpy as np

def nothing(x):
    pass

out = "./person.idl"
f_out = open(out, 'a+')

link = "./S1.avi"
cap = cv2.VideoCapture(link)
# cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, 500000)
bg = []
cv2.namedWindow('threshold') 
cv2.createTrackbar('thresh','threshold',0,255,nothing)
cv2.setTrackbarPos('thresh','threshold', 35)
flag = False
zm = 1
cntr =0
unique ="sv"
wait = 50
write_img = True

while True:
	ret, img = cap.read()
	if ret:
		# print img.shape
		img = cv2.resize(img, (640,480))
		img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img_grey = cv2.blur(img_grey,(5,5))

		if flag:
			imdiff = cv2.absdiff(img_grey, bg)
			thresh = cv2.getTrackbarPos('thresh','threshold')
			_, fg = cv2.threshold(imdiff,thresh,255,cv2.THRESH_BINARY)

			kernel = np.ones((5,13),np.uint8) 
			open1 = cv2.morphologyEx(fg, cv2.MORPH_OPEN,np.ones((5,5),np.uint8), iterations = 1)
			close = cv2.morphologyEx(open1,cv2.MORPH_CLOSE,kernel, iterations = 5)
			close = cv2.dilate(close, np.ones((5,13),np.uint8), iterations = 2)
			close2 = close.copy()

			_, contours, hierarchy = cv2.findContours(close2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			persons = []
			img2 = img.copy()
			for cnt in contours:
				area = cv2.contourArea(cnt)
				if area>6000:
					x,y,w,h = cv2.boundingRect(cnt)
					cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
					if h>150 and float(h)/w >= 1.50:
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
						persons.append((x,y, x+w, y+h))
					# print h, float(h)/w, 

			sav = './Person/'+unique + str(cntr)+'.jpg'
			write_line = '"'+sav + '":'
			for (x,y, x2, y2) in persons:
				write_line += ' ('+ str(x) +','+ str(y) +','+ str(x2) + ','+ str(y2) + ')'

			if len(persons)>0 and write_img:
				cv2.imwrite(sav, img2)
				print write_line
				f_out.write(write_line)
				f_out.write(';\n')
				cntr += 1

			cv2.imshow('threshold', fg)
			cv2.imshow('ooi', close)
		cv2.imshow('frame', img)

	else :
		print "Error: reading frame"

	key = cv2.waitKey(wait)
	if key == 27:
		break
	if key == ord('b'):
		flag = True
		bg = img_grey.copy()
	if key == ord('q'):
		flag = False
	if key == ord('z'):
		write_img = False
		wait = 0
	if key == ord('s') and write_img == False:
		cv2.imwrite(sav, img2)
		print write_line
		f_out.write(write_line)
		f_out.write(';\n')
		cntr += 1
	if key == ord('a'):
		write_img = True
		wait = 50