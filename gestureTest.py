import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# BaseOptions = mp.tasks.BaseOptions
# GestureRecognizer = mp.tasks.vision.GestureRecognizer
# GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
# GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
# VisionRunningMode = mp.tasks.vision.RunningMode

# # Create a gesture recognizer instance with the live stream mode:
# def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
#     print('gesture recognition result: {}'.format(result))

# options = GestureRecognizerOptions(
#     base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
#     running_mode=VisionRunningMode.LIVE_STREAM,
#     result_callback=print_result)
# with GestureRecognizer.create_from_options(options) as recognizer:
  # The detector is initialized. Use it here.
  # ...

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the image mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.IMAGE)
with GestureRecognizer.create_from_options(options) as recognizer:
  # The detector is initialized. Use it here.
  # ...

    # Load the input image from an image file.
    mp_image = mp.Image.create_from_file('thumbs-up-2649310_640.jpg')

    # Perform gesture recognition on the provided single image.
    # The gesture recognizer must be created with the image mode.
    gesture_recognition_result = recognizer.recognize(mp_image)
    print(gesture_recognition_result.gestures)
    print(gesture_recognition_result.handedness)
    # print(gesture_recognition_result.hand_landmarks)