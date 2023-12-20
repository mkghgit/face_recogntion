import cv2
import face_recognition
import os

# Create a folder to store face images
output_folder = "face_and_telebot"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize variables
person_id_counter = 1

# Function to capture a photo and save face image


def capture_and_save_face():
    global person_id_counter

    # Open the default camera (0)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Press "c" to capture', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Capture an image if 'c' is pressed
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Find face locations in the frame
            face_locations = face_recognition.face_locations(frame)

            if face_locations:
                # Take the first face found
                top, right, bottom, left = face_locations[0]

                # Crop and save the face image

                with open("numbxx.txt", "r", encoding="UTF-8") as filexx1:
                    content = filexx1.read()
                nn = content
                with open("numbxx.txt", "w", encoding="UTF-8") as filexx2:
                    content_plus = filexx2.write(str(int(nn)+1))

                print(f"____________{nn}_____________________")

                face_image = frame[top:bottom, left:right]
                cv2.imwrite(os.path.join(output_folder,
                            f"person_{nn}.jpg"), face_image)

                print(f"Person {person_id_counter} captured!")

                # Increment the person ID counter
                person_id_counter += 1

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()


# Capture and save faces
capture_and_save_face()
