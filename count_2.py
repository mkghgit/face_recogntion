import face_recognition
import os
import cv2
import numpy as np



# Folder containing the captured face images
images_folder = "face_and_telebot"
# Function to load face images and IDs


def load_face_images_and_ids(folder):
    face_images = []
    person_ids = []

    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            path = os.path.join(folder, filename)
            face_image = face_recognition.load_image_file(path)
            face_encoding = face_recognition.face_encodings(face_image)[0]

            # Extract the person ID from the filename (person_1.jpg -> 1)
            person_id = int(os.path.splitext(filename)[0].split('_')[1])

            face_images.append(face_encoding)
            person_ids.append(person_id)

    return np.array(face_images), np.array(person_ids)


# Load face images and IDs
known_face_encodings, known_person_ids = load_face_images_and_ids(
    images_folder)

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Find face locations in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        person_id = "Unknown"

        if True in matches:
            # Find the index of the first matching face
            first_match_index = matches.index(True)
            person_id = known_person_ids[first_match_index]

        # Draw rectangle and person ID on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, f"Person ID: {
                    person_id}", (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
