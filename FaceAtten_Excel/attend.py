import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
#use of os:provide a host of other funtions that allow
#you to interact with the opearting system

#importing Images
path='ImagesAt'
images=[]
classNames=[]
mylist=os.listdir(path)
print(mylist)

for cl in mylist:
    curImg=cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    #cl is our classname of every image
    #to print the name without jpg we use 'splitext'
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

#to find encodings

def findEncodings(images):
    encodeList=[]

    #first convert it into rgb ,then count the images in the list through face encodings

    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
#Now Marking the attendance
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# print(myDataList)




encodeListKnown=findEncodings(images)
print('Encoding Complete')

#Step-3:Finding cmparison

cap=cv2.VideoCapture(0)

while True:
    success,img=cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#In VideoCamera it may happen that multiple faces can occur,so in that case we
    #have to find out the face to be comparison
    facesCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace )
        print(faceDis)
        matchIndex=np.argmin(faceDis)
#Stored the indexes in array,if it matches then print the name
        if matches[matchIndex]:
            name=classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1=faceLoc
            # MAy OCCUr problem due to scaling down the image comparison pragma,to revive this multiply by 4
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
#Making the bounding box


    cv2.imshow('WebCam',img)
    cv2.waitKey(1)
#THIS loop will basically grab the face location and face encodings,using 'zip' because we want them in the same loop



