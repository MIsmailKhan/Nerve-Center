import cv2
import numpy as np

#roi = cv2.imread('/home/saurabh/Documents/Codes/Python/OpenCV/brown.png')
#hsvb = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
#roi = cv2.imread('/home/saurabh/Documents/Codes/Python/OpenCV/white.png')
#hsvw = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
#
## calculating object histogram
#roihist_brown = cv2.calcHist([hsvb],[0, 1], None, [30, 30], [0, 180, 0, 256] )
#roihist_white = cv2.calcHist([hsvw],[1, 2], None, [30, 30], [0, 256, 0, 256] )
## normalize histogram and apply backprojection
#cv2.normalize(roihist_brown,roihist_brown,0,255,cv2.NORM_MINMAX)
#cv2.normalize(roihist_white,roihist_white,0,255,cv2.NORM_MINMAX)

b_lower = np.array([18,32,40])
b_upper = np.array([32,230,213])
w_lower = np.array([0,0,125])
w_upper = np.array([120,100,200])
Standstill_rate = 0.03
HeatMap_rate = 0.03

cap = cv2.VideoCapture("C:\Users\MohammadIsmail\Desktop\TestVideo\Docket.mp4")
for i in range(10000):
	#target = cv2.imread('/home/saurabh/Documents/Codes/Python/OpenCV/trolly.png')
	
	ret,target = cap.read()
	hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
	if i ==0:
		backgound = hsvt[:,:,2]
		Standstill_im = np.zeros(backgound.shape)
		prev_image =  np.zeros(backgound.shape,dtype='uint8')
		HeatMap_im = np.zeros(backgound.shape)
		continue

	bg_diff = cv2.absdiff(hsvt[:,:,2], backgound)
	bg_blur = cv2.blur(bg_diff,(5,5))
	ret,bg_thresh = cv2.threshold(bg_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# dstb = cv2.calcBackProject([hsvt],[0,1],roihist_brown,[0,180,0,256],1)
	# dstw = cv2.calcBackProject([hsvt],[1,2],roihist_white,[0,256,0,256],1)
		
	# dst = cv2.bitwise_or(dstb,dstw)

	# hist_blur = cv2.blur(dst,(5,5))
	# ret,hist_thresh = cv2.threshold(hist_blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# Now convolute with circular disc
	#disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
	#cv2.filter2D(dst,-1,disc,dst)

	hist_thresh = cv2.inRange(hsvt,b_lower,b_upper)
	hist_thresh = cv2.morphologyEx(hist_thresh, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
	white_thresh = cv2.inRange(hsvt,w_lower,w_upper)
	#hist_thresh = cv2.bitwise_or(hist_thresh,white_thresh)
	
	# threshold and binary AND
	thresh = cv2.bitwise_and(hist_thresh,bg_thresh)
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
	threshRGB = cv2.merge((thresh,thresh,thresh))
	res = cv2.bitwise_and(target,threshRGB)
	
	#Standstill
	Standstill_im = (1-Standstill_rate) * Standstill_im + Standstill_rate * thresh
	Standstill_im =  cv2.bitwise_and(Standstill_im.astype('uint8'), thresh)
	_,sthresh = cv2.threshold(Standstill_im,200,255,cv2.THRESH_BINARY_INV)
	thresh_standstill = cv2.bitwise_and(thresh, cv2.bitwise_not(sthresh))


	#HeatMap
	imdiff = cv2.absdiff(thresh, prev_image)
	prev_image = thresh
	HeatMap_im = cv2.scaleAdd(imdiff, 5, ((1-HeatMap_rate)*HeatMap_im).astype('uint8'))



	#Contour



	#Bounding box



	#res1 = np.vstack((target,cv2.merge((dst,dst,dst)),thresh,res))
	cv2.imshow("target", target)
	#cv2.imshow("dst", dst)
	#cv2.imshow("bg_thresh", bg_thresh)
	#cv2.imshow("hist_thresh", hist_thresh)
	#cv2.imshow("thresh", thresh)
	#cv2.imshow("result", res)

	#cv2.imshow("sthresh", sthresh)
	cv2.imshow("HeatMap_im", HeatMap_im)
	#cv2.imshow("result_standstill", thresh_standstill)
	cv2.waitKey(3)
#cv2.imwrite('res1.jpg',res1)
cv2.waitKey(10000)