##) principal steps
#1) Read image
#2) Low Blur Filtering
#3) Grayscale
#4) High Filtering
#5) Morphologic Operation: Dilate
#6) find Contourns

import cv2
import numpy as np
import os
import PySimpleGUI as sg
fig_size=[640,480]

#settings show Camera
cap = cv2.VideoCapture(0)
cap.set(3,fig_size[0])  # channel 3: windows width
cap.set(4,fig_size[1])  # channel 4: windows height
Gaussian_Kernel=(9,9)
Dil_kelnel=np.ones((9,9))
def nothing(x):
    pass
cv2.namedWindow('Parameters')
cv2.createTrackbar('Thres_low', 'Parameters', 0, 255, nothing)
cv2.createTrackbar('Thres_upp', 'Parameters', 0, 255, nothing)
cv2.createTrackbar('Area', 'Parameters', 1000, 30000, nothing)
cv2.createTrackbar('Iterations', 'Parameters', 1, 10, nothing)

#initialize infinite cycle
if cap.isOpened():
    CtrlRead, image = cap.read()
    while True:
        thr1=cv2.getTrackbarPos("Thres_low","Parameters")
        thr2=cv2.getTrackbarPos('Thres_upp',"Parameters")
        CtrlRead, frame = cap.read()                                #1)
        RGBContors=frame.copy()
        frame_Hbf=cv2.GaussianBlur(frame,Gaussian_Kernel,1)         #2)
        frame_Gray=cv2.cvtColor(frame_Hbf, cv2.COLOR_BGR2GRAY)      #3)
        frame_Edge=cv2.Canny(frame_Gray,thr1,thr2)                  #4)
        iterMin=cv2.getTrackbarPos('Iterations',"Parameters")
        frame_MorD=cv2.dilate(frame_Edge,Dil_kelnel,iterations=iterMin)   #5)
        contours,hierarchy=cv2.findContours(frame_MorD,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(RGBContors,contours,-1,(250,250,100),2)
        for cont in contours:
            Area=cv2.contourArea(cont)
            areaMin=cv2.getTrackbarPos('Area',"Parameters")
            if Area>areaMin:
                cv2.drawContours(RGBContors,cont,-1,(255,0,255),5)
                perimetr=cv2.arcLength(cont,True)
                Round=cv2.approxPolyDP(cont,0.02*perimetr,True)
                x1,y1,w1,h1=cv2.boundingRect(Round)
                cv2.rectangle(RGBContors, (x1,y1),(x1+w1,y1+h1),(0,244,0),1)
                cv2.putText(RGBContors,"Points:"+str(len(Round)),(x1+w1+30,y1+30),cv2.FONT_HERSHEY_COMPLEX ,.8,(0,0,255),3)
                cv2.putText(RGBContors,"Area:"+str(int(Area)),(x1+w1+30,y1+70),cv2.FONT_HERSHEY_COMPLEX,.8,(0,0,255),3)



        imgHor = np.hstack((frame_Edge,frame_MorD))
        imgHorRGB = np.hstack((frame,RGBContors))
        imgHorResize = cv2.resize(imgHor,(int(imgHor.shape[1]/2),int(imgHor.shape[0]/2)))
        frameResize = cv2.resize(frame,(int(frame.shape[1]/2),int(frame.shape[0]/2)))
        imgHorRGBResize = cv2.resize(imgHorRGB,(int(imgHorRGB.shape[1]/2),int(imgHorRGB.shape[0]/2)))
        cv2.imshow("original",imgHorRGBResize)
        cv2.imshow("Gray-Edge",imgHorResize)




        key = cv2.waitKey(1)   
        if key == 27 or key==ord('q'): 
            break
folder = sg.popup_get_folder('File Name','File Search')   
os.chdir(folder)
cv2.imwrite("Detect_RGB.png", imgHorRGBResize)
cv2.imwrite("Detect_Edge.png", imgHorResize)
cap.release()
cv2.destroyAllWindows()
