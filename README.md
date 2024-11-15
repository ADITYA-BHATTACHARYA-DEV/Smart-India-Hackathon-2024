Madhya Pradesh Police Tracking System: Installation Guide
Welcome to the Madhya Pradesh Police Tracking System! This advanced AI-based facial recognition and attendance management system is designed to streamline and automate the attendance process. In this guide, we’ll walk you through the necessary steps to install and set up the system on your local machine.

Prerequisites
Before you begin, make sure you have the following:

1. Python 3.7+
The code is written in Python 3, so ensure you have Python 3.7 or above installed on your machine. You can download the latest version of Python from the official Python website.

2. pip (Python Package Installer)
pip is the package manager for Python. Ensure that you have the latest version installed. You can upgrade pip using:

bash
Copy code
python -m pip install --upgrade pip
3. Additional Tools
Some packages, like OpenCV, require additional tools to be installed.

CMake: Required for building OpenCV from source. Download and install CMake from here.

Visual Studio (Windows-only): If you're on Windows, you will need Visual Studio with C++ build tools to compile OpenCV. You can download Visual Studio from here.

Step-by-Step Installation
Step 1: Clone the Repository
First, you’ll need to clone the GitHub repository that contains the code.

bash
Copy code
git clone https://github.com/your-repository-link.git
cd your-repository-folder
Step 2: Set Up a Virtual Environment (Recommended)
Setting up a virtual environment will help you manage the dependencies without affecting the global Python installation.

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
Step 3: Install Required Libraries
You can either use a requirements.txt file (if provided) or install the necessary libraries manually.

Option 1: Using requirements.txt
Create a file named requirements.txt in the project folder with the following contents:

txt
Copy code
streamlit
opencv-python
face_recognition
numpy
pandas
plotly
pillow
Now, install the dependencies with this command:

bash
Copy code
pip install -r requirements.txt
Option 2: Manually Installing Libraries
If the requirements.txt is not available, manually install the necessary libraries using the following command:

bash
Copy code
pip install streamlit opencv-python face_recognition numpy pandas plotly pillow
Library Details
Here’s a breakdown of the essential libraries used in the system:

Streamlit:
Used for creating the interactive web application where you can manage and track attendance.

Installation: pip install streamlit
Streamlit Documentation
OpenCV:
This library handles image processing, capturing video input, and performing facial recognition tasks.

Installation: pip install opencv-python
OpenCV Documentation
face_recognition:
A powerful library for face detection and recognition. It compares uploaded images to detect known faces.

Installation: pip install face_recognition
face_recognition Documentation
NumPy:
A fundamental package for scientific computing with Python. It is used for handling and manipulating image data as arrays.

Installation: pip install numpy
NumPy Documentation
Pandas:
This library is used for managing and manipulating attendance data in CSV format.

Installation: pip install pandas
Pandas Documentation
Plotly:
Used to generate interactive plots and data visualizations for attendance analytics.

Installation: pip install plotly
Plotly Documentation
Pillow:
Pillow is a fork of Python Imaging Library (PIL). It handles image operations such as opening, manipulating, and displaying images in Streamlit.

Installation: pip install pillow
Pillow Documentation
Additional Notes
Image Directory Setup
Make sure to create a folder named ImagesAt in your project directory. This folder should contain the images of individuals whose attendance will be recorded.

Attendance File
The system will automatically generate an Attendance.csv file in the working directory to store attendance records. This file will be created upon the first attendance entry.

Camera Setup
The system uses your webcam to capture video feed and perform facial recognition. Ensure that your camera is connected and accessible.

Running the Application
Once all dependencies are installed, you can start the application with the following command:

bash
Copy code
streamlit run Prime_Main.py
This will launch the Streamlit app in your default web browser, where you can interact with the tracking system.

Troubleshooting
Face Recognition Issues: If you encounter issues with the face_recognition library (e.g., due to missing dependencies or CMake errors), make sure you have installed the required tools like CMake and Visual Studio (for Windows users).

Webcam Access: Ensure your system allows webcam access for the Python script. If you’re using Streamlit, you may need to grant permissions.

Conclusion
With these steps, you’ll be able to set up the Madhya Pradesh Police Tracking System on your machine. This system leverages facial recognition technology to efficiently manage attendance for police personnel.

For any questions or issues, please refer to the GitHub repository or open an issue for support.
