import cv2
import numpy as np

class roi_mouse:
    def __init__(self):
        self.init_point = (0, 0)
        self.final_point = (0, 0)
        self.frame = []
        self.crop = []
        self.track_window = []
        self.drawing = False
        self.count = 600            	
        self.xoff, self.yoff = 30, 30

def draw_rect_with_mouse(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        param.drawing = True
        param.init_point = (x,y)
        print 'start', param.init_point

    elif event == cv2.EVENT_MOUSEMOVE:
        if param.drawing == True:
            move = np.copy(param.frame)
            cv2.rectangle(move, param.init_point, (x,y), (255,0,0), 1)
            cv2.imshow("Video", move)

    elif event == cv2.EVENT_LBUTTONUP:
        param.drawing = False
        param.final_point = (x,y)
        cv2.rectangle(param.frame, param.init_point, param.final_point,(0,0,255), 1)
        print 'end', param.final_point
        img = param.frame[param.init_point[1]:param.final_point[1], param.init_point[0]:param.final_point[0]]
        cv2.imshow("crop", img)
        param.crop = img

def run_main(src):
	rect = roi_mouse()
	cap = cv2.VideoCapture(src)
	cap.set(cv2.CAP_PROP_POS_MSEC, 2100000)
	window = "Video"
	mark_area = roi_mouse()
	cv2.namedWindow(window)
	cv2.setMouseCallback(window, draw_rect_with_mouse, mark_area)
	state = 'playing'

	while True:
		if cap.isOpened() and state == 'playing':
			ret, im = cap.read()
			if ret: mark_area.frame = np.copy(im)
			else: print 'Error: Reading frame'

		cv2.imshow("Video", mark_area.frame)

		key = cv2.waitKey(0)
		if key == ord(' '):
			if state == 'playing':
				state = 'paused'
			else:
				state = 'playing'

		if key == ord('s'):
			img = im[mark_area.init_point[1]:mark_area.final_point[1], mark_area.init_point[0]:mark_area.final_point[0]]
			cv2.imwrite("./positive_images/" + str(mark_area.count)+".jpg", img)
			cv2.destroyWindow("crop")
			print "Saved ", mark_area.count, ".jpg"
			mark_area.count += 1

		if key == ord('q'):
			mark_area.frame = np.copy(im)
			cv2.destroyWindow("crop")

		if key == 27:
			break

if __name__ == "__main__":
    run_main("HCVR_ch32_main_20160723080001_20160723090003.asf")
    # run_main("rtsp://admin:admin@223.31.30.53:554/cam/realmonitor?channel=19&subtype=00")