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
dragStartPoint = (0,0)
lastMovePoint = (0,0)
previousPreciseCords = (0,0)
preciseFrameBuffer = settings.preciseFrameBufferThreshold
dragFrameBuffer = settings.dragFrameBufferThreshold

# Create a image segmenter instance with the live stream mode:
def mouseFunctions(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global leftClicked
    global rightClicked
    global middleClicked
    global dragStartPoint
    global lastMovePoint
    global previousPreciseCords
    global preciseFrameBuffer
    global dragFrameBuffer

    hand_landmarks_list = result.hand_landmarks # is list with one list in it that has all landmarks

    if(len(hand_landmarks_list) > 0): # if there is a hand recognized in view
        middleOfHand = hand_landmarks_list[0][9] # removes outer list layer and gets middle finger knuckle landmark
        gesture = result.gestures[0][0].category_name # stores recognized hand gesture
        handXCord = 1 - middleOfHand.x # camera feed is flipped horizontaly so must minus from 1 to match x coordinate with pixel coordinate system (top left of screen = 0,0)
        handYCord = middleOfHand.y
        handZCord = middleOfHand.z # even though middle finger knuckle landmark is being used here z coordinate is always calculated based on distance of wrist landmark to camera

        # resets checks to allow these types of clicks again
        if(leftClicked == 1 or rightClicked == 1 or middleClicked == 1): # this if with nested ifs/elifs allows less if checks per frame when needing to reset a click
            if(leftClicked == 1 and not(gesture == "Pointing_Up")):
                leftClicked = 0
            elif(rightClicked == 1 and not(gesture == "Victory")):
                rightClicked = 0
            elif(middleClicked == 1 and not(gesture == "Closed_Fist")):
                middleClicked = 0

        if(dragFrameBuffer < settings.dragFrameBufferThreshold and not(gesture == "ILoveYou")): # FINSISHED DRAGGING CHECK: comes before checking gestures as it must execute a drag before respodning to other input if the user is dragging
            dragFrameBuffer += 1
            if(dragFrameBuffer == settings.dragFrameBufferThreshold and not(gesture == "ILoveYou")): # reached only when dragFrameBuffer reaches threshold but before next frame - needs to be nested to as condition is always true when not dragging
                mouse.drag(dragStartPoint[0], dragStartPoint[1], mouse.get_position()[0], mouse.get_position()[1], absolute = True, duration = settings.dragSpeed) # DRAG MOUSE FUNCTION: drags the mouse from the stored coordinates where the drag was initiated to where the drag has ended

        match gesture: # match case structure to dictate what to do for each gesture
            case "Open_Palm": # MOVING AND PRECISELY MOVING MOUSE
                
                if(handZCord >= settings.preciseMovementThreshold and preciseFrameBuffer >= settings.preciseFrameBufferThreshold): # MOVING MOUSE: hand is far enough from camera and has not been precise moving for at certain number of frames
                    if(((abs(lastMovePoint[0] - handXCord) > settings.minMovedDistance)) or (abs(lastMovePoint[1] - handYCord) > settings.minMovedDistance)): # JITTERY MOUSE PREVENTION: see README
                        mouse.move((((handXCord * 1.71429) - 0.357143) * settings.screenResolution[0]), (((handYCord * 1.71429) - 0.357143) * settings.screenResolution[1]), absolute=True, duration=0) # MOVE MOUSE FUNCTION: see README
                        lastMovePoint = (handXCord, handYCord) # used for jittery mouse prevention
                
                elif(handZCord >= settings.preciseMovementThreshold): # INCREMENT FRAME BUFFER: only reached if far enough from camera but was precisely moving within 15 frames
                    preciseFrameBuffer += 1
                
                else: # PRECISELY MOVING MOUSE: hand is close enough to camera
                    if(preciseFrameBuffer == settings.preciseFrameBufferThreshold): # only true if first entering precise moving mode and sets previous point
                        previousPreciseCords = (handXCord, handYCord)
                    elif(abs(handXCord - previousPreciseCords[0]) > settings.minPreciseMovedDistance or abs(handYCord - previousPreciseCords[1]) > settings.minPreciseMovedDistance): # JITTERY MOUSE PREVENTION: see README
                        mouse.move((handXCord - previousPreciseCords[0]) * settings.preciseMovementSpeed, (handYCord - previousPreciseCords[1]) * settings.preciseMovementSpeed, absolute = False, duration  = 0) # PRECISE MOVE MOUSE FUNCTION: see README
                        previousPreciseCords = (handXCord, handYCord)
                    preciseFrameBuffer = 0 # PRECISE FRAME BUFFER: see README

            case "ILoveYou": # DRAGGING AND PRECISELY DRAGGING MOUSE
                
                if(dragFrameBuffer == settings.dragFrameBufferThreshold): # only true if first entering dragging and sets point to start dragging from
                    dragStartPoint = mouse.get_position()
                dragFrameBuffer = 0 # DRAG FRAME BUFFER: prevents premature executing of drag due to single frames occasionaly un recognizing hand gesture similar to precise frame buffer (see README for precise frame buffer)
                
                # proceeding block identical to block in Open_Palm case
                if(handZCord >= settings.preciseMovementThreshold and preciseFrameBuffer >= settings.preciseFrameBufferThreshold): # MOVING MOUSE: hand is far enough from camera and has not been precise moving for at certain number of frames
                    if(((abs(lastMovePoint[0] - handXCord) > settings.minMovedDistance)) or (abs(lastMovePoint[1] - handYCord) > settings.minMovedDistance)): # JITTERY MOUSE PREVENTION: see README
                        mouse.move((((handXCord * 1.71429) - 0.357143) * settings.screenResolution[0]), (((handYCord * 1.71429) - 0.357143) * settings.screenResolution[1]), absolute=True, duration=0) # MOVE MOUSE FUNCTION: see README
                        lastMovePoint = (handXCord, handYCord) # used for jittery mouse prevention
                elif(handZCord >= settings.preciseMovementThreshold): # INCREMENT FRAME BUFFER: only reached if far enough from camera but was precisely moving within 15 frames
                    preciseFrameBuffer += 1
                else: # PRECISELY MOVING MOUSE: hand is close enough to camera
                    if(preciseFrameBuffer == settings.preciseFrameBufferThreshold): # only true if first entering precise moving mode and sets previous point
                        previousPreciseCords = (handXCord, handYCord)
                    elif(abs(handXCord - previousPreciseCords[0]) > settings.minPreciseMovedDistance or abs(handYCord - previousPreciseCords[1]) > settings.minPreciseMovedDistance): # JITTERY MOUSE PREVENTION: see README
                        mouse.move((handXCord - previousPreciseCords[0]) * settings.preciseMovementSpeed, (handYCord - previousPreciseCords[1]) * settings.preciseMovementSpeed, absolute = False, duration  = 0) # PRECISE MOVE MOUSE FUNCTION: see README
                        previousPreciseCords = (handXCord, handYCord)
                    preciseFrameBuffer = 0 # PRECISE FRAME BUFFER: see README
            
            case "Pointing_Up": # LEFT CLICKING

                if(leftClicked == 0): # allows only the first frame the gesture is recognized to click 
                    mouse.click("left")
                    leftClicked = 1
            
            case "Victory": # RIGHT CLICKING
                
                if(rightClicked == 0): # allows only the first frame the gesture is recognized to click 
                    mouse.click("right")
                    rightClicked = 1
            
            case "Closed_Fist": # MIDDLE CLICKING
                
                if(middleClicked == 0): # allows only the first frame the gesture is recognized to click
                    mouse.click("middle")
                    middleClicked = 1
            
            case "Thumb_Up": # SCROLLING UP
                
                mouse.wheel(settings.scrollSpeed)
            
            case "Thumb_Down": # SCROLLING DOWN
                
                mouse.wheel(-1 * settings.scrollSpeed) # negative values scroll down
            
            case _: # UNRECOGNIZED
                pass


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