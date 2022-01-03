##) principal steps
#1) Read image
#2) Low Blur Filtering
#3) Grayscale
#4) High Filtering
#5) Morphologic Operation: Dilate
#6) find Contourns

import cv2
import numpy as np
fig_size=[640,480]

#settings show Camera
cap = cv2.VideoCapture(0)
cap.set(3,fig_size[0])  # channel 3: windows width
cap.set(4,fig_size[1])  # channel 4: windows height
Gaussian_Kernel=(9,9)
def nothing(x):
    pass
cv2.namedWindow('Parameters')
cv2.createTrackbar('Thres_low', 'Parameters', 0, 255, nothing)
cv2.createTrackbar('Thres_upp', 'Parameters', 0, 255, nothing)

#initialize infinite cycle
if cap.isOpened():
    CtrlRead, image = cap.read()
    while True:
        thr1=cv2.getTrackbarPos("Thres_low","Parameters")
        thr2=cv2.getTrackbarPos('Thres_upp',"Parameters")
        CtrlRead, frame = cap.read()                            #1)
        frame_Hbf=cv2.GaussianBlur(frame,Gaussian_Kernel,1)     #2)
        frame_Gray=cv2.cvtColor(frame_Hbf, cv2.COLOR_BGR2GRAY)  #3)
        frame_Edge=cv2.Canny(frame_Gray,thr1,thr2)              #4)
        imgHor = np.hstack((frame_Gray,frame_Edge))
        imgHorResize = cv2.resize(imgHor,(int(imgHor.shape[1]/2),int(imgHor.shape[0]/2)))
        frameResize = cv2.resize(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)))
        cv2.imshow("original",frameResize)
        cv2.imshow("Gray-Edge",imgHorResize)




        key = cv2.waitKey(1)   
        if key == 27 or key==ord('q'): 
            break
#folder = sg.popup_get_folder('File Name','File Search')   #4
#os.chdir(folder)
#cv2.imwrite("Detect_RGB.png", frame)
#cv2.imwrite("Detect_Subtract.png", ImgSub)
cap.release()
cv2.destroyAllWindows()
