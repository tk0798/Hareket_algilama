import numpy as np
import cv2 as cv
import Person
import time

try:
    log = open('log.txt',"w")
except:
    print("log.txt kaydedilmedi")

#yukarı aşağı capraz giren çıkan sayaçları
cnt_up   = 0
cnt_down = 0
cnt_capraz = 0

cap = cv.VideoCapture("ch04_20210901083004 (online-video-cutter.com).mp4")
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1300)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1300)

for i in range(19):
    print(i, cap.get(i))

h = 480
w = 640
frameArea = h*w
areaTH = frameArea/250
print( 'eşik :', areaTH)

#Yukarı aşağı sınırlar
# line_up = int(2*(h/5))
# line_down = int(3*(h/5))

# up_limit =   int(1*(h/5))
# down_limit = int(4*(h/5))
line_up =250
line_down =500
up_limit =200
down_limit =1300

line_down_color = (255,0,0)
line_up_color = (0,0,255)
# pt1 =  [0, line_down]
# pt2 =  [w, line_down]
pt1 =  [0, 500]
pt2 =  [1300, 500]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [600, 250]
pt4 =  [1300, 250]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))
pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

#filtreler
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

while(cap.isOpened()):
    ret, frame = cap.read()
    # height, width = frame.shape[:2]
    # rotation_matrix = cv.getRotationMatrix2D((width/2, height/2), -9, .9)
    # frame = cv.warpAffine(frame, rotation_matrix, (width, height))

    #frame = cv.rotate(frame, cv.ROTATE_180)
    # cv.line(frame,(0,0),(640,480),(45,89,126),3)

    for i in persons:
        i.age_one()

    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    try:
        ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
        ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)

        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)

        mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print('UP:',cnt_up)
        print('DOWN:',cnt_down)
        print("CAPRAZ",cnt_capraz)
        break


    contours0, hierarchy = cv.findContours(mask2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt)
        if area > 1998:

            M = cv.moments(cnt)
            cx = int(M['m10']/M['m00'])

            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv.boundingRect(cnt)
            x_up_limit= 0
            x_down_limit = 1100
            x_line_up=0
            x_line_down=1000
            new = True
            if cx in range(x_up_limit,x_down_limit):
                if cy in range(up_limit,down_limit):
                    for i in persons:
                        if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                            new = False
                            i.updateCoords(cx,cy)
                            if i.going_UP(line_down,line_up,x_line_up,x_line_down) == True:
                                cnt_up += 1
                                log.write("ID: "+str(i.getId())+' yukarıya doğru ' + time.strftime("%c") + '\n')
                                cv.imwrite('fotolar\\up' + str(i.getId()) + '.jpg', frame)
                            elif i.going_DOWN(line_down,line_up,x_line_up,x_line_down) == True:
                                cnt_down += 1
                                log.write("ID: " + str(i.getId()) + ' aşağıya doğru ' + time.strftime("%c") + '\n')
                                cv.imwrite('fotolar\\down' + str(i.getId()) + '.jpg', frame)
                            elif i.deneme(line_down, line_up, x_line_up, x_line_down) == True:
                                cnt_capraz += 1
                                log.write("ID: " + str(i.getId()) + ' capraz doğru ' + time.strftime("%c") + '\n')
                                cv.imwrite('fotolar\\capraz' + str(i.getId()) + '.jpg', frame)
                            break
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < up_limit:
                                i.setDone()

                        if i.timedOut():

                            index = persons.index(i)
                            persons.pop(index)
                            del i
                    if new == True:
                        p = Person.MyPerson(pid,cx,cy, max_p_age)
                        persons.append(p)
                        pid += 1

            cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


    for i in persons:

        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)

    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    str_capraz = 'CAPRAZ: '+ str(cnt_capraz)

    frame = cv.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
    # frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    # frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    cv.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv.LINE_AA)
    cv.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv.LINE_AA)
    cv.putText(frame, str_capraz ,(10,140),font,0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_capraz ,(10,140),font,0.5,(0,255,0),1,cv.LINE_AA)

    cv.line(frame, (0, 400), (1000, 150), (45, 89, 126), 3)


    cv.imshow('Frame',frame)
    cv.imshow('Mask',mask2)

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

log.flush()
log.close()
cap.release()
cv.destroyAllWindows()

