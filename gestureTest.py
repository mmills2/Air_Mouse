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
rightClicked = 0
middleClicked = 0
dragStarted = 0
dragStartPoint = (0,0)
lastMovePoint = (0,0)
currentlyMoving = 0
preciseStartPoint = (0,0)
currentlyPreciseMoving = 0

def resetChecks(): # cant get this called in callback
    leftClicked = 0
    rightClicked = 0
    middleClicked = 0
    currentlyMoving = 0
    currentlyPreciseMoving = 0

# Create a image segmenter instance with the live stream mode:
def mouseFunctions(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global leftClicked
    global rightClicked
    global middleClicked
    global dragStarted
    global dragStartPoint
    global lastMovePoint
    global currentlyMoving
    global preciseStartPoint
    global currentlyPreciseMoving

    # cv2.imshow('Show', output_image.numpy_view())
    # imright = output_image.numpy_view()
    gestureList = result.gestures
    hand_landmarks_list = result.hand_landmarks # is list with one list in it that has all landmarks
    if(len(hand_landmarks_list) > 0):
        print(gestureList[0][0].category_name)
        hand_landmarks = hand_landmarks_list[0][9] # removes outer list layer and gets middle of hand
        # print("x:",hand_landmarks.x)
        print("z:", hand_landmarks.z)
        if (gestureList[0][0].category_name == "Open_Palm"):
            if(currentlyMoving == 1):
                if(((abs(lastMovePoint[0] - (1 - hand_landmarks.x)) > 0.003)) or (abs(lastMovePoint[1] - hand_landmarks.y) > 0.003)):
                    if(hand_landmarks.z < -0.04):
                        if(currentlyPreciseMoving == 1):
                            if(abs((1 - hand_landmarks.x) - preciseStartPoint[0]) > 0.01 or abs(hand_landmarks.y - preciseStartPoint[1]) > 0.01):
                                mouse.move(((1 - hand_landmarks.x) - preciseStartPoint[0]) * 100, (hand_landmarks.y - preciseStartPoint[1]) * 100, absolute = False, duration  = 0.01)
                                # print(((1 - hand_landmarks.x) - preciseStartPoint[0]) * 100, (hand_landmarks.y - preciseStartPoint[1]) * 100)
                                preciseStartPoint = (1 - hand_landmarks.x, hand_landmarks.y)
                        else:
                            preciseStartPoint = (1 - hand_landmarks.x, hand_landmarks.y)
                            currentlyPreciseMoving = 1
                    else:
                        mouse.move(((((1 - hand_landmarks.x) * 1.71429) - 0.357143) * 1382), (((hand_landmarks.y * 1.71429) - 0.357143) * 864), absolute=True, duration=0) # 1382 x 864 is currently my own screen resolution (only that small because its scaled 250%) I want to change this to get the machine's screen size (not sure how I will account for scaling though)
                        currentlyPreciseMoving = 0
                    lastMovePoint = (1 - hand_landmarks.x, hand_landmarks.y)
            else:
                currentlyMoving = 1
                mouse.move((((1 - hand_landmarks.x) * 1.71429) - 0.357143) * 1382, ((hand_landmarks.y * 1.71429) - 0.357143) * 864, absolute=True, duration=0)
                lastMovePoint = (1 - hand_landmarks.x, hand_landmarks.y)
            if(dragStarted == 1):
                mouse.drag(dragStartPoint[0], dragStartPoint[1], mouse.get_position()[0], mouse.get_position()[1], absolute = True, duration = 0.1)
                dragStarted = 0
        elif (gestureList[0][0].category_name == "Pointing_Up"):
            if(leftClicked == 0):
                mouse.click("left")
                leftClicked = 1
        elif (gestureList[0][0].category_name == "Victory"):
            if(rightClicked == 0):
                mouse.click("right")
                rightClicked = 1
        elif (gestureList[0][0].category_name == "Closed_Fist"):
            if(middleClicked == 0):
                mouse.click("middle")
                middleClicked = 1
        elif (gestureList[0][0].category_name == "Thumb_Up"):
            mouse.wheel(0.5)
        elif (gestureList[0][0].category_name == "Thumb_Down"):
            mouse.wheel(-0.5)
        elif (gestureList[0][0].category_name == "ILoveYou"):
            if(dragStarted == 0):
                dragStartPoint = mouse.get_position()
                dragStarted = 1
            if(((abs(lastMovePoint[0] - (1 - hand_landmarks.x)) > 0.003)) or (abs(lastMovePoint[1] - hand_landmarks.y) > 0.003)):
                    mouse.move((((1 - hand_landmarks.x) * 1.71429) - 0.357143) * 1382, ((hand_landmarks.y * 1.71429) - 0.357143) * 864, absolute=True, duration=0) # 1382 x 864 is currently my own screen resolution (only that small because its scaled 250%) I want to change this to get the machine's screen size (not sure how I will account for scaling though)
                    lastMovePoint = (1 - hand_landmarks.x, hand_landmarks.y)
            currentlyMoving = 0
        else:
            leftClicked = 0
            rightClicked = 0
            middleClicked = 0
            currentlyMoving = 0
            currentlyPreciseMoving = 0

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

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray) # replace second frame with gray for grayscale

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