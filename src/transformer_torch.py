from picamera import PiCamera
from time import sleep
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def detect_mood(text):
    vs = analyzer.polarity_scores(text)
    compound = vs['compound']

    if compound >= 0.5:
        mood = "Happy"
    elif compound <= -0.5:
        mood = "Sad"
    else:
        mood = "Neutral"

    print(f"The detected mood is: {mood} (Compound score: {compound})")
    return mood

# Initialize the camera
my_camera = PiCamera()
my_camera.resolution = (1920, 1080)  # Full HD resolution
my_camera.vflip = True  # Vertical flip
my_camera.hflip = True  # Horizontal flip

print('Taking a 5-second video clip...')

# Start recording
my_camera.start_preview()
my_camera.start_recording('video.h264')
sleep(5)  # Record for 5 seconds
my_camera.stop_recording()
my_camera.stop_preview()

print('Done recording.')

# Example mood input
mood_input = "I feel really excited and joyful today!"

# Run the mood detection function
detect_mood(mood_input)