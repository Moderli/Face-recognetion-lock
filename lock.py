import cv2
import face_recognition
import os
import pickle
from base64 import b64encode, b64decode
import numpy as np
import ast
import json

def encode_content(content, face_data):
    encoded_content = b64encode(content.encode('utf-8')).decode('utf-8')
    
    # Convert the face encoding to a list
    face_encoding_list = face_data['face_encoding'].tolist()
    
    # Combine the encoded content with face data for additional security
    encoded_data = f"{face_encoding_list}:{encoded_content}"
    
    return encoded_data

def decode_content(encoded_data, face_encodings):
    face_encoding_str, encoded_content = encoded_data.split(':', 1)

    # Clean up the face encoding string and convert it to a NumPy array
    face_encoding_str = face_encoding_str.replace('[', '').replace(']', '')
    face_encoding_list = [float(val) for val in face_encoding_str.split(',')]
    face_encoding = np.array(face_encoding_list)

    if face_recognition.compare_faces([face_encoding], face_encodings[0])[0]:
        return b64decode(encoded_content).decode('utf-8')
    else:
        return None

def register_face(username):
    # Open camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Find face locations and face encodings
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if face_encodings:
            # Save face encoding along with the username
            data = {"username": username, "face_encoding": face_encodings[0]}
            with open(f"{username}_face_data.pkl", "wb") as file:
                pickle.dump(data, file)

            print(f"Face registered for user: {username}")
            break

        # Display the resulting frame
        cv2.imshow('Register Face', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def lock_file(username, file_path):
    # Load the registered face data
    face_data_file = f"{username}_face_data.pkl"
    if not os.path.exists(face_data_file):
        print("User not registered. Please register your face first.")
        return

    with open(face_data_file, "rb") as file:
        face_data = pickle.load(file)

    # Read and encode the content of the file
    with open(file_path, 'r') as file_to_lock:
        content = file_to_lock.read()
        encoded_content = encode_content(content, face_data)

    # Save the encoded content to a new file
    locked_file_path = f"{file_path}_locked"
    with open(locked_file_path, 'w') as locked_file:
        locked_file.write(encoded_content)

    # Delete the existing file
    os.remove(file_path)
    
    print(f"File locked for user: {username}")
    print(f"Locked file saved at: {locked_file_path}")
    print(f"Original file '{file_path}' deleted.")

def unlock_file(username, file_path):
    # Load the registered face data
    face_data_file = f"{username}_face_data.pkl"
    if not os.path.exists(face_data_file):
        print("User not registered. Please register your face first.")
        return

    with open(face_data_file, "rb") as file:
        face_data = pickle.load(file)

    # Attempt to open the specified file
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("Adding '_locked' to the file path and trying again.")
        file_path = f"{file_path}_locked"

    # Open camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Find face locations and face encodings
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        if face_encodings:
            # Compare the face encoding with the registered face
            result = face_recognition.compare_faces([np.array(face_data["face_encoding"])], face_encodings[0])

            if result[0]:
                # Read and decode the content of the locked file
                with open(file_path, 'r') as locked_file:
                    encoded_content = locked_file.read()
                    decoded_content = decode_content(encoded_content, face_encodings)

                if decoded_content is not None:
                    print(f"File unlocked for user: {username}")
                    print(f"Decoded content:\n{decoded_content}")
                    # Your code to use the unlocked content goes here
                else:
                    print("Face not recognized. File remains locked.")
                    # Your code for unauthorized access goes here

                break

        # Display the resulting frame
        cv2.imshow('Unlock File', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def main():
    while True:
        print("Choose an option:")
        print("1. Register Face")
        print("2. Lock File")
        print("3. Unlock File")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            username = input("Enter your username: ")
            register_face(username)
        elif choice == '2':
            username = input("Enter your username: ")
            file_path = input("Enter the file path to lock: ")
            lock_file(username, file_path)
        elif choice == '3':
            username = input("Enter your username: ")
            file_path = input("Enter the file path to unlock: ")
            unlock_file(username, file_path)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
