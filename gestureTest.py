import mediapipe as mp
import cv2
import mouse

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)

leftClicked = 0

# Create a image segmenter instance with the live stream mode:
def mouseFunctions(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global leftClicked
    # cv2.imshow('Show', output_image.numpy_view())
    # imright = output_image.numpy_view()
    gestureList = result.gestures
    hand_landmarks_list = result.hand_landmarks # is list with one list in it that has all landmarks
    if(len(hand_landmarks_list) > 0):
        print(gestureList[0][0].category_name)
        hand_landmarks = hand_landmarks_list[0][9] # removes outer list layer and gets middle of hand
        print("x:",hand_landmarks.x)
        print("y:",hand_landmarks.y)
        if (gestureList[0][0].category_name == "Open_Palm"):
            mouse.move((1 - hand_landmarks.x) * 1382, hand_landmarks.y * 864, absolute=True, duration=0) # 1382 x 864 is currently my own screen resolution (only that small because its scaled 250%) I want to change this to get the machine's screen size (not sure how I will account for scaling though)
        elif (gestureList[0][0].category_name == "Pointing_Up"):
            if(leftClicked == 0):
                mouse.click("left")
                leftClicked = 1
        else:
            leftClicked = 0

        


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=mouseFunctions)

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    while video.isOpened(): 
        # Capture frame-by-frame
        ret, frame = video.read()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)

        if cv2.waitKey(5) & 0xFF == 27:
            break

video.release()
cv2.destroyAllWindows()