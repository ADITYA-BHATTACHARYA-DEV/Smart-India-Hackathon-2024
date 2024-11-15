import cv2
import numpy as np
import face_recognition

 # Step-1:Loading The Images and Converting it into RGB because we are getting the image as bgr

imgScarlett=face_recognition.load_image_file("Images/Scarlett.jpg")
imgScarlett=cv2.cvtColor(imgScarlett,cv2.COLOR_BGR2RGB)
imgkat=face_recognition.load_image_file("Images/Kat.jpg")
imgkat=cv2.cvtColor(imgkat,cv2.COLOR_BGR2RGB)

#Comparing the Above loaded image with passed value

imgScarlettTest=face_recognition.load_image_file("Images/scarlett-johansson.jpg")
imgScarlettTest=cv2.cvtColor(imgScarlettTest,cv2.COLOR_BGR2RGB)

#Step-2:Finding our Face in the given picture and finding their encodings repectively

faceLoc=face_recognition.face_locations(imgScarlett)[0]
#Single Image is passed with single element

encodeScarlet=face_recognition.face_encodings(imgScarlett)[0]
cv2.rectangle(imgScarlett,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
print(faceLoc)
#top,right,bottom,left
faceLoc1=face_recognition.face_locations(imgkat)[0]
#Single Image is passed with single element

encodekat=face_recognition.face_encodings(imgkat)[0]
cv2.rectangle(imgkat,(faceLoc1[3],faceLoc1[0]),(faceLoc1[1],faceLoc1[2]),(255,0,255),2)
print(faceLoc1)


faceLocTest=face_recognition.face_locations(imgScarlettTest)[0]
#Single Image is passed with single element

encodeScarletTest=face_recognition.face_encodings(imgScarlettTest)[0]
cv2.rectangle(imgScarlettTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
print(faceLocTest)

#Step-3:Comparing these two images

results=face_recognition.compare_faces([encodeScarlet,encodekat],encodeScarletTest)
#To match the best/exact facial expression -to do that we will find the difference
# between the encodings-lower the distance better the match is

faceDis=face_recognition.face_distance([encodeScarlet,encodekat],encodeScarletTest)

print(results,faceDis)





cv2.putText(imgScarlettTest,f'{results}{round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
#use of imshow:To Display the image which is loaded
cv2.imshow('SCARLETT',imgScarlett)
cv2.imshow('Kat',imgkat)
cv2.imshow('SCARLETT.J',imgScarlettTest)
cv2.waitKey(0)
#use of waitkey :-to display window for specified time,if value passed is zero then it means that the window is displayd until any key is pressed
