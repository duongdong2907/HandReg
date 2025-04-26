import cv2
import mediapipe as mp
import time
import os
import hand as htm

previous_time=0 
cap=cv2.VideoCapture(0)

width=1280
height=720

cap.set(3,width) #set width
cap.set(4,height) #set height

region_top=100
region_bottom=600
region_left=900
region_right=1220

hand=None
FolderPath = "Fingers"
lst=os.listdir(FolderPath)
lst_2=[] #make list
for i in lst:
    image=cv2.imread(f'{FolderPath}/{i}')
    print(f'{FolderPath}/{i}')
    lst_2.append(image)


detector= htm.handDetector(detectionCon=0.55)

fingerid=[4,8,12,16,20] #Finger tip id
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    #print(lmList)

    #vẽ vùng để tay vào
    cv2.rectangle(frame, (region_left, region_top), (region_right, region_bottom), (255,255,0), 2)
    
    if len(lmList)!=0:
        #Check xem tay có ở trong vùng không
        hand_center_x = lmList[9][1]
        hand_center_y = lmList[9][2]
        if region_left < hand_center_x < region_right and region_top < hand_center_y < region_bottom:
            fingers=[] #tạo list

            #ngón cái
            if lmList[fingerid[0]][1] < lmList[fingerid[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            #4 ngón tay (trừ ngón cái)
            for id in range(1,5):
                if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalFingers=fingers.count(1)
        else:
            if hand==None or hand.isInFrame==False:
                cv2 .putText(frame, "No hand detected", (1100,20), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255 , 255 , 255 ),1,cv2.LINE_AA)
            else:
                totalFingers=0
    else:
        totalFingers=0
        cv2 .putText(frame, "No hand detected", (1100,20), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255 , 255 , 255 ),1,cv2.LINE_AA)
    

    if totalFingers > 0 and totalFingers <= len(lst_2):
        h,w,c=lst_2[totalFingers-1].shape #gán định dạng ảnh vào h,w,c
        frame[0:h,0:w]=lst_2[totalFingers-1] #chèn ảnh ngón tay
    
    
    
    #vẽ hình chữ nhật hiện số ngón tay
    cv2.rectangle(frame,(0,225),(170,425),(255,0,0),cv2.FILLED)
    cv2.putText(frame,str(totalFingers),(38,375),cv2.FONT_HERSHEY_SIMPLEX,5,(255,255,0),3)


    #FPS
    current_time = time.time() #thời gian hiện tại
    fps = 1/(current_time - previous_time) #fps
    previous_time = current_time #gán thời gian hiện tại cho thời gian trước đó
    #show fps lên màn hình
    cv2.putText(frame, f'FPS: {int(fps)}', (200, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): #bấm q để thoát chương trình
        break

cap.release() 
cv2.destroyAllWindows()
