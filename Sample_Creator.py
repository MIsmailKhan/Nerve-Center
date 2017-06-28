
cap.set(cv2.CAP_PROP_POS_MSEC, 5*60*1000)import cv2
import numpy as np

def nothing(x):
    pass

out = "./17bagismail.idl"
f_out = open(out, 'a+')

link = "HCVR_ch17_main_20160802160200_20160802170000.asf"
cap = cv2.VideoCapture(link)
bg = []
cv2.namedWindow('threshold')
cv2.createTrackbar('thresh','threshold',0,255,nothing)
cv2.setTrackbarPos('thresh','threshold', 35)
flag = False
zm = 1
cntr =1
unique ="17ultron"
wait = 50
write_img = True

class roi_mouse:
    def __init__(self):
        self.init_point = []
        self.final_point = []
        self.frame = []
        self.crop = ""
        self.track_window = []
        self.drawing = False

def draw_rect_with_mouse(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        param.drawing = True
        param.init_point = (x,y)
        print 'start', param.init_point
        mark_area.crop += ' ('+ str(x) +','+ str(y) +','

    elif event == cv2.EVENT_MOUSEMOVE:
        if param.drawing == True:
            move = np.copy(param.frame)
            cv2.rectangle(move, param.init_point, (x,y), (255,0,0), 1)
            cv2.imshow("frame", move)

    elif event == cv2.EVENT_LBUTTONUP:
        param.drawing = False
        param.final_point = (x,y)
        cv2.rectangle(param.frame, param.init_point, param.final_point,(0,0,255), 2)
        cv2.imshow("frame", param.frame)
        print 'end', param.final_point
        mark_area.crop += str(x) + ','+ str(y) + ')'

window = "frame"
mark_area = roi_mouse()
cv2.namedWindow(window)
cv2.setMouseCallback(window, draw_rect_with_mouse, mark_area)

while True:
	ret, img = cap.read()
	if ret:
		# print img.shape
		img = cv2.resize(img, (640,480))
		img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img_grey = cv2.blur(img_grey,(5,5))

		sav = './Bag17/'+unique + str(cntr)+'.jpg'
		write_line = '"'+sav + '":'
		mark_area.crop = write_line
		img2 = img.copy()

		if flag:
			imdiff = cv2.absdiff(img_grey, bg)
			thresh = cv2.getTrackbarPos('thresh','threshold')
			_, fg = cv2.threshold(imdiff,thresh,255,cv2.THRESH_BINARY)

			kernel = np.ones((5,13),np.uint8)
			open1 = cv2.morphologyEx(fg, cv2.MORPH_OPEN,np.ones((5,5),np.uint8), iterations = 1)
			close = cv2.morphologyEx(open1,cv2.MORPH_CLOSE,kernel, iterations = 5)
			close = cv2.dilate(close, np.ones((5,13),np.uint8), iterations = 2)
			close2 = close.copy()

			_,contours, hierarchy = cv2.findContours(close2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
			persons = []
			for cnt in contours:
				area = cv2.contourArea(cnt)
				if area>1000:
					x,y,w,h = cv2.boundingRect(cnt)
					cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
					if h>150 and float(h)/w <= 1.50:
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
						persons.append((x,y, x+w, y+h))
					# print h, float(h)/w,

			for (x,y, x2, y2) in persons:
				write_line += ' ('+ str(x) +','+ str(y) +','+ str(x2) + ','+ str(y2) + ')'
				mark_area.crop = write_line

			if len(persons)>0 and write_img:
				cv2.imwrite(sav, img2)
				print write_line
				f_out.write(write_line)
				f_out.write(';\n')
				cntr += 1

			cv2.imshow('threshold', fg)
			cv2.imshow('ooi', close)

		mark_area.frame = np.copy(img)
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
		print mark_area.crop
		f_out.write(mark_area.crop)
		f_out.write(';\n')
		cntr += 1
	if key == ord('a'):
		flag = True
		write_img = True
		wait = 50
	if key == ord('c'):
		write_line = '"'+sav + '":'
		mark_area.crop = write_line
		persons = []