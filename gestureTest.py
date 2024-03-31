import mediapipe as mp
import cv2
import mouse
import settings

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)

leftClicked = 0
rightClicked = 0
middleClicked = 0
isDragging = 0
dragStartPoint = (0,0)
lastMovePoint = (0,0)
isLastMovePointSet = 0
previousPreciseCords = (0,0)
currentlyPreciseMoving = 0
preciseFrameBuffer = 15

def adjustForScreenEdges(landmarkCord):
    return (landmarkCord * 1.71429) - 0.357143

def resetChecks():
    global leftClicked
    global rightClicked
    global middleClicked
    global isLastMovePointSet
    leftClicked = 0
    rightClicked = 0
    middleClicked = 0
    isLastMovePointSet = 0

# Create a image segmenter instance with the live stream mode:
def mouseFunctions(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global leftClicked
    global rightClicked
    global middleClicked
    global isDragging
    global dragStartPoint
    global lastMovePoint
    global isLastMovePointSet
    global previousPreciseCords
    global currentlyPreciseMoving
    global preciseFrameBuffer
    global adjustForScreenEdges

    gestureList = result.gestures
    hand_landmarks_list = result.hand_landmarks # is list with one list in it that has all landmarks
    if(len(hand_landmarks_list) > 10):
        print(gestureList[0][0].category_name)
        middleOfHand = hand_landmarks_list[0][9] # removes outer list layer and gets middle of hand
        print("x:",middleOfHand.x)
        print("z:", middleOfHand.z)
        if(currentlyPreciseMoving == 1 and middleOfHand.z >= -0.04 and preciseFrameBuffer < 15):
            preciseFrameBuffer += 1
            print(preciseFrameBuffer)
        elif(currentlyPreciseMoving == 1 and middleOfHand.z >= -0.04 and preciseFrameBuffer >= 15):
            currentlyPreciseMoving = 0
        if(not(gestureList[0][0].category_name == "ILoveYou") and isDragging == 1):
            mouse.drag(dragStartPoint[0], dragStartPoint[1], mouse.get_position()[0], mouse.get_position()[1], absolute = True, duration = 0.1)
            isDragging = 0
        elif (gestureList[0][0].category_name == "Open_Palm"):
            if(isLastMovePointSet == 1):
                if(((abs(lastMovePoint[0] - (1 - middleOfHand.x)) > 0.003)) or (abs(lastMovePoint[1] - middleOfHand.y) > 0.003)):
                    if(middleOfHand.z < -0.04):
                        if(currentlyPreciseMoving == 1):
                            preciseFrameBuffer = 0
                            if(abs((1 - middleOfHand.x) - previousPreciseCords[0]) > 0.01 or abs(middleOfHand.y - previousPreciseCords[1]) > 0.01):
                                mouse.move(((1 - middleOfHand.x) - previousPreciseCords[0]) * 150, (middleOfHand.y - previousPreciseCords[1]) * 150, absolute = False, duration  = 0.01)
                                previousPreciseCords = (1 - middleOfHand.x, middleOfHand.y)
                        else:
                            previousPreciseCords = (1 - middleOfHand.x, middleOfHand.y)
                            currentlyPreciseMoving = 1
                    else:
                        mouse.move(((((1 - middleOfHand.x) * 1.71429) - 0.357143) * 1382), (((middleOfHand.y * 1.71429) - 0.357143) * 864), absolute=True, duration=0) # 1382 x 864 is currently my own screen resolution (only that small because its scaled 250%) I want to change this to get the machine's screen size (not sure how I will account for scaling though)
                    lastMovePoint = (1 - middleOfHand.x, middleOfHand.y)
            else:
                isLastMovePointSet = 1
                mouse.move((((1 - middleOfHand.x) * 1.71429) - 0.357143) * 1382, ((middleOfHand.y * 1.71429) - 0.357143) * 864, absolute=True, duration=0)
                lastMovePoint = (1 - middleOfHand.x, middleOfHand.y)
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
            if(isDragging == 0):
                dragStartPoint = mouse.get_position()
                isDragging = 1
            if(((abs(lastMovePoint[0] - (1 - middleOfHand.x)) > 0.003)) or (abs(lastMovePoint[1] - middleOfHand.y) > 0.003)):
                    if(middleOfHand.z < -0.04):
                        if(currentlyPreciseMoving == 1):
                            preciseFrameBuffer = 0
                            if(abs((1 - middleOfHand.x) - previousPreciseCords[0]) > 0.01 or abs(middleOfHand.y - previousPreciseCords[1]) > 0.01):
                                mouse.move(((1 - middleOfHand.x) - previousPreciseCords[0]) * 150, (middleOfHand.y - previousPreciseCords[1]) * 150, absolute = False, duration  = 0.01)
                                # print(((1 - middleOfHand.x) - previousPreciseCords[0]) * 100, (middleOfHand.y - previousPreciseCords[1]) * 100)
                                previousPreciseCords = (1 - middleOfHand.x, middleOfHand.y)
                        else:
                            previousPreciseCords = (1 - middleOfHand.x, middleOfHand.y)
                            currentlyPreciseMoving = 1
                    else:
                        mouse.move((((1 - middleOfHand.x) * 1.71429) - 0.357143) * 1382, ((middleOfHand.y * 1.71429) - 0.357143) * 864, absolute=True, duration=0) # 1382 x 864 is currently my own screen resolution (only that small because its scaled 250%) I want to change this to get the machine's screen size (not sure how I will account for scaling though)
                        lastMovePoint = (1 - middleOfHand.x, middleOfHand.y)
            isLastMovePointSet = 0
        else:
            resetChecks()
    if(len(hand_landmarks_list) > 0): # if there is a hand recognized in view
        middleOfHand = hand_landmarks_list[0][9] # removes outer list layer and gets middle finger knuckle landmark
        gesture = gestureList[0][0].category_name # stores recognized hand gesture
        handXCord = 1 - middleOfHand.x # camera feed is flipped horizontaly so must minus from 1 to match x coordinate with pixel coordinate system (top left of screen = 0,0)
        handYCord = middleOfHand.y
        handZCord = middleOfHand.z # even though middle finger knuckle landmark is being used here z coordinate is always calculated based on distance of wrist landmark to camera

        if(isDragging == 1 and not(gesture == "ILoveYou")): # FINSISHED DRAGGING CHECK: comes before checking gestures as it must execute a drag before respodning to other input if the user is dragging
            mouse.drag(dragStartPoint[0], dragStartPoint[1], mouse.get_position()[0], mouse.get_position()[1], absolute = True, duration = settings.dragSpeed) # DRAG MOUSE FUNCTION: drags the mouse from the stored coordinates where the drag was initiated to where the drag has ended
            isDragging = 0

        match gesture: # match case structure to dictate what to do for each gesture
            case "Open_Palm": # MOVING AND PRECISELY MOVING MOUSE
                if(handZCord >= settings.preciseMovementThreshold and preciseFrameBuffer >= settings.preciseFrameBufferThreshold): # MOVING MOUSE: hand is far enough from camera and has not been precise moving for at certain number of frames
                    if(((abs(lastMovePoint[0] - handXCord) > settings.minMovedDistance)) or (abs(lastMovePoint[1] - handYCord) > settings.minMovedDistance)): # JITTERY MOUSE PREVENTION: see README
                        mouse.move((adjustForScreenEdges(handXCord) * settings.screenResolution[0]), (adjustForScreenEdges(handYCord) * settings.screenResolution[1]), absolute=True, duration=0) # MOVE MOUSE FUNCTION: see README
                        lastMovePoint = (handXCord, handYCord) # used for jittery mouse prevention
                elif(handZCord >= settings.preciseMovementThreshold): # INCREMENT FRAME BUFFER: only reached if far enough from camera but was precisely moving within 15 frames
                    preciseFrameBuffer += 1
                else: # PRECISELY MOVING MOUSE: hand is close enough to camera
                    if(preciseFrameBuffer == 15): # only true if first entering precise moving mode and sets previous point
                        previousPreciseCords = (handXCord, handYCord)
                    elif(abs(handXCord - previousPreciseCords[0]) > 0.01 or abs(handYCord - previousPreciseCords[1]) > 0.01): # JITTERY MOUSE PREVENTION: see README
                        mouse.move((handXCord - previousPreciseCords[0]) * settings.preciseMovementSpeed, (handYCord - previousPreciseCords[1]) * settings.preciseMovementSpeed, absolute = False, duration  = 0) # PRECISE MOVE MOUSE FUNCTION: see README
                        previousPreciseCords = (handXCord, handYCord)
                    preciseFrameBuffer = 0 # PRECISE FRAME BUFFER: see README
            case "ILoveYou": # DRAGGING AND PRECISELY DRAGGING MOUSE
                print(gesture)
            case "Pointing_Up": # LEFT CLICKING
                print(gesture)
            case "Victory": # RIGHT CLICKING
                print(gesture)
            case "Closed_Fist": # MIDDLE CLICKING
                print(gesture)
            case "Thumb_Up": # SCROLLING UP
                print(gesture)
            case "Thumb_Down": # SCROLLING DOWN
                print(gesture)
            case _: # UNRECOGNIZED
                print("Not recognized")



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