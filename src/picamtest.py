from picamera import PiCamera
import cv2
import numpy as np
from fer import FER
from time import sleep, time
from threading import Thread
import io

# Initialize components
camera = PiCamera()
camera.resolution = (640, 480)
camera.vflip = True
camera.hflip = True

# Emotion detector
detector = FER(mtcnn=True)

# Shared variables
running = True
frame_buffer = io.BytesIO()

# Function to continuously read and analyze frames
def analyze_stream():
    global running
    stream = io.BytesIO()

    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        if not running:
            break

        # Convert to NumPy array
        stream.seek(0)
        data = np.frombuffer(stream.read(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)

        # Detect emotion
        result = detector.top_emotion(image)
        if result:
            mood, score = result
            label = f'{mood} ({int(score * 100)}%)'
        else:
            label = 'Mood: Unknown'

        # Draw overlay
        cv2.rectangle(image, (0, 0), (640, 40), (0, 0, 0), -1)
        cv2.putText(image, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Display
        cv2.imshow('Mood AI Preview', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

        stream.seek(0)
        stream.truncate()

# Start video recording
print("Starting video recording and mood analysis...")
camera.start_preview()
camera.start_recording('video.h264')

# Start emotion detection in background thread
thread = Thread(target=analyze_stream)
thread.start()

# Record for 5 seconds
sleep(5)
running = False
thread.join()

# Cleanup
camera.stop_recording()
camera.stop_preview()
cv2.destroyAllWindows()

print("Recording and mood display complete.")