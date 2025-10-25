# Hand Gesture Volume Control 🎚️✋

A Python project that controls system volume using hand gestures detected by a webcam.

## Tech Stack
- Python
- OpenCV
- Mediapipe
- Handtrack
- PyCAW
- NumPy

## How It Works
The system tracks your hand using Mediapipe, measures the distance between your thumb and index finger, and maps it to your computer’s master volume.

## Run It
```bash
pip install -r requirements.txt

python VolumeHandControl.py
