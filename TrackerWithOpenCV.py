import cv2


width=640
height= 480
#settings show Camera
cap = cv2.VideoCapture(0)
cap.set(3,width)  # channel 3: windows width
cap.set(4,heigth)  # channel 4: windows height

#initialize infinite cycle
if cap.isOpened():
    CtrlRead, image = cap.read()
    while True:
        CtrlRead, frame = cap.read()
        cv2.imshow("cam",frame)



        key = cv2.waitKey(1)   
        if key == 27 or key==ord('q'): 
            break
#folder = sg.popup_get_folder('File Name','File Search')   #4
#os.chdir(folder)
#cv2.imwrite("Detect_RGB.png", frame)
#cv2.imwrite("Detect_Subtract.png", ImgSub)
cap.release()
cv2.destroyAllWindows()
