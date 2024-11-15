from datetime import datetime, date
import streamlit as st
import dlib
import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
path='ImagesAt'
st.title("Face Attendance System")


# st.text("Please Stand infront of the camera")

#Error Element
st.success("Please Stand in front of the Camera")

# Sidebar
st.sidebar.header('Class Attendance')
st.sidebar.subheader('Present Date and Time ')

# Date Input
date = st.sidebar.date_input('Present Date', datetime.today())

# Time Input
time = st.sidebar.time_input('Current Time', datetime.now().time())
stop_button_pressed=st.sidebar.button("Stop")

images=[]
#Write all the names
classNames=[]
myList=os.listdir(path)
#The above line of code separates andlosts every element in the folder
print(myList)

for cl in myList:
    #Current Image
    curImg=cv2.imread(f'{path}/{cl}')
    #cl is the name of our image
    images.append(curImg)
    #For splitting the path text and grabbing the first element
    classNames.append(os.path.splitext(cl)[0])
# print(classNames)


#Now finding Encodings
def findEncodings(images):
    # Now creating an empty list that will have all the encodings
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #Now finding the encodings
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            today=date.today()
            formated_date=today.strftime('%B, %d, %Y')
            dtString=now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{formated_date},{dtString}')

# print(myDataList)

    # print(myDataList)


encodeListKnown=findEncodings(images)
print('Encoding Complete')

cap=cv2.VideoCapture(0)


def load_data(data) -> pd.DataFrame:
    return pd.read_csv(data)


st.sidebar.success("Marked Attendance")
df = load_data("Attendance.csv")
st.sidebar.dataframe(df)
#The purpose of loop is to read every frame one by one
while cap.isOpened() and not stop_button_pressed:
    ret,img=cap.read()
    if not ret:
        st.write("The Video capture has ended")
        break
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # frame_placeholder.image(img, channels="RGB")
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    #To find encoding of out webcam
    facesCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)
    #Now finding the matches
    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
        # print(faceDis)
        # It will give a list of face differences when matching through the webcam,each photo is compared with the photos of the list and the webcam

        # It will one by one grab the faces current list compare the encodings of the images
        # Since we want them all in the same loop , we are using 'ZIP"

        matchIndex=np.argmin(faceDis)

        #Creating the bounding Box around the matched Input
        if matches[matchIndex]:
            name=classNames[matchIndex].upper()
            # print(name)
            y1,x2,y2,x1=faceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,255))
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
            # print(success)
            markAttendance(name)

            cv2.imshow('WebCam', img)



            if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
                break

cap.release()


cv2.destroyAllWindows()














