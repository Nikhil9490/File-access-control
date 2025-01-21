import cv2
import face_recognition
import os
import ctypes
import tkinter as tk
from tkinter import simpledialog

# Load images and encode faces
image_admin1 = face_recognition.load_image_file(r"C:\Users\nikhi\OneDrive\Desktop\admin1.jpg")
encoding_admin1 = face_recognition.face_encodings(image_admin1)[0]

image_admin2 = face_recognition.load_image_file(r"C:\Users\nikhi\OneDrive\Desktop\admin2.jpg")
encoding_admin2 = face_recognition.face_encodings(image_admin2)[0]

image_admin3 = face_recognition.load_image_file(r"C:\Users\nikhi\OneDrive\Desktop\admin3.jpg")
encoding_admin3 = face_recognition.face_encodings(image_admin3)[0]

# Create arrays of known face encodings and corresponding names
known_face_encodings = [encoding_admin1, encoding_admin2, encoding_admin3]
known_face_names = ["admin1", "admin2", "admin3"]

# Capture video from the default camera
video_capture = cv2.VideoCapture(0)

current_user = "Unknown"

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match is found, use the name of the first matching known face
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # Update the recognized user
            current_user = name

    # Draw rectangle and name on the video feed
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if current_user == "Unknown":
            # Ask security question
            root = tk.Tk()
            root.withdraw()
            answer = simpledialog.askstring("Security Question", "Where were you born?")
            root.destroy()

            # Determine user based on the answer
            if answer in ["hyd", "Hyderabad"]:
                current_user = "admin1"
            elif answer in ["mlg", "Malaga"]:
                current_user = "admin2"
            elif answer in ["kdd", "Kadapa"]:
                current_user = "admin3"
            else:
                current_user = "unknown"

        break

# Release the video capture object and close the window
video_capture.release()
cv2.destroyAllWindows()

print(f"Recognized user: {current_user}")

def hide_folder(folder_path):
    ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)

# Hide folders based on recognized user
if current_user == "admin1":
    hide_folder(r"C:\Users\nikhi\OneDrive\Desktop\pictures")
    hide_folder(r"C:\Users\nikhi\OneDrive\Desktop\videos")
elif current_user == "admin2":
    hide_folder(r"C:\Users\nikhi\OneDrive\Desktop\docs")
    hide_folder(r"C:\Users\nikhi\OneDrive\Desktop\pictures")
elif current_user == "admin3":
    hide_folder(r"C:\Users\nikhi\OneDrive\Desktop\videos")
    hide_folder(r"C:\Users\nikhi\OneDrive\Desktop\docs")
elif current_user == "unknown":
    # Trigger sleep mode
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
