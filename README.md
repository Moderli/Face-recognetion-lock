# FaceLock

FaceLock is a simple Python script that allows users to lock and unlock files using face recognition. It utilizes the face_recognition library for face detection and encoding.

## Features

- **Face Registration:** Register your face by capturing and storing your face encoding.
- **File Locking:** Lock a specified file with your registered face.
- **File Unlocking:** Unlock a previously locked file by verifying your face.

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- face_recognition (`pip install face_recognition`)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/FaceLock.git
   cd FaceLock
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:

   ```bash
   python main.py
   ```

4. Follow the on-screen instructions to register your face, lock, and unlock files.

## Options

- **Register Face (Option 1):** Capture and store your face encoding for future recognition.
- **Lock File (Option 2):** Lock a specified file with your registered face.
- **Unlock File (Option 3):** Unlock a previously locked file by verifying your face.
- **Exit (Option 4):** Quit the application.

## Notes

- Make sure to have a working webcam for face registration and verification.
- The application creates a pickle file (`username_face_data.pkl`) to store face encoding data.

## License

This project is licensed under the [MIT License](LICENSE).

