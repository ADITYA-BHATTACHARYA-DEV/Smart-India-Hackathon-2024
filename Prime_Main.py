from datetime import datetime, date
import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
import plotly.express as px
from PIL import Image

# Configuration and Styling
st.set_page_config(page_title="MP Police Attendance System", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #0047AB; font-family: Arial;'>Madhya Pradesh Police Attendance System</h1>",
    unsafe_allow_html=True
)

# Sidebar with Attendance, Date-Time, and Image Upload
st.sidebar.header('Attendance System')
st.sidebar.subheader('Present Date and Time')
current_date = st.sidebar.date_input('Present Date', datetime.today())
current_time = st.sidebar.time_input('Current Time', datetime.now().time())
stop_button_pressed = st.sidebar.button("Stop Attendance System")

# Image upload for new entries
st.sidebar.subheader("Add New Images")
uploaded_image = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Path for images and initialize lists
path = 'ImagesAt'
images, classNames = [], []
myList = os.listdir(path)

# Save uploaded images to 'ImagesAt' directory and reload image list
if uploaded_image is not None:
    new_image_path = os.path.join(path, uploaded_image.name)
    with open(new_image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    st.sidebar.success("Image uploaded successfully!")
    myList = os.listdir(path)  # Refresh image list after upload

# Load images and class names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])


# Encode known faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            continue  # Skip images where no face is detected
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'a') as f:
        now = datetime.now()
        today = date.today()
        formatted_date = today.strftime('%B %d, %Y')
        dtString = now.strftime('%H:%M:%S')
        f.write(f'\n{name},{formatted_date},{dtString}')


# Load encoded images
encodeListKnown = findEncodings(images)
st.sidebar.success("Face Encodings Loaded Successfully!")


# Load or create attendance DataFrame
def load_data():
    try:
        return pd.read_csv("Attendance.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Date", "Time"])


df = load_data()

# Sidebar - Attendance History and Bar Graph
st.sidebar.subheader("Attendance History")
st.sidebar.dataframe(df)

# Setup Video Capture and Display
cap = cv2.VideoCapture(0)
frame_placeholder = st.empty()  # Camera frame placeholder
status_placeholder = st.empty()  # Success message placeholder

# Center camera feed and placeholder for attendance log
with st.container():
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    frame_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# Table to Display Identified People with Date and Time
attendance_log = pd.DataFrame(columns=["Photo", "Name", "Date", "Time"])
marked_names = set()  # Set to track already marked individuals

# Attendance Processing Loop
while cap.isOpened() and not stop_button_pressed:
    ret, img = cap.read()
    if not ret:
        st.warning("Video capture ended.")
        break

    # Resize image for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Face locations and encodings
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Draw rectangle and text
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            # Check if the person is already marked
            if name not in marked_names:
                # Mark attendance and add entry to log
                markAttendance(name)
                marked_names.add(name)  # Add to set to prevent re-marking

                now = datetime.now()
                formatted_date = now.strftime("%B %d, %Y")
                formatted_time = now.strftime("%H:%M:%S")

                # Load person's saved image
                img_path = os.path.join(path, f"{name.lower()}.jpg")
                person_img = Image.open(img_path) if os.path.exists(img_path) else None

                # Append to log table
                attendance_log = pd.concat([attendance_log, pd.DataFrame({
                    "Photo": [person_img],
                    "Name": [name],
                    "Date": [formatted_date],
                    "Time": [formatted_time]
                })])

                # Show success message
                status_placeholder.success(f"{name} marked present!")
            else:
                # Show message for already marked
                status_placeholder.info(f"{name} already marked.")

    # Update camera frame display
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(img_rgb, channels="RGB")

    # Update attendance table in real-time
    st.markdown("<h2 style='text-align: center;'>Attendance Log</h2>", unsafe_allow_html=True)
    st.write(attendance_log[["Name", "Date", "Time"]])  # Display basic log table
    st.image(attendance_log["Photo"].tolist(), width=100, caption=attendance_log["Name"].tolist())

    # Stop capturing if the button is pressed
    if stop_button_pressed:
        break

cap.release()
cv2.destroyAllWindows()

# Footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: black;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-family: Arial, sans-serif;
        }
    </style>
    <div class="footer">
        © 2024 Madhya Pradesh Police | Powered by Aditya Bhattacharya 
    </div>
""", unsafe_allow_html=True)
