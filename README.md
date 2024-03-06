# Air Mouse

Air Mouse lets you control your mouse using your camera to track your hand and recognize hand gestures. The mouse matches the movement of your hand and the recognized hand gestures control different mouse functions like left and right click.

## How to Install

To begin, you must have **Python version 3.10** installed. You can either downgrade/upgrade your Python version to match this version or create a virtual environment with Python 3.10.
Next, you will have to install two libraries: MediaPipe and mouse. MediaPipe is a library that utilizes artificial intelligence and machine learning for a wide range of solutions but this project will only use the hand tracking and gesture recognition soltuion. mouse is a library that allows you to programmatically control your mouse.

### Libraries

To install MediaPipe, run the following command in your command line: 
```
python -m pip install mediapipe
```
To install mouse, run the following command in your command line:
```
python -m pip install mouse
```

Now that you have the correct version of Python and the libraries installed, you're good to download this project's code and run the code in your programming environment.

## How to use

To get the best results for all hand gestures, orientate your hand so your palm is facing the camera and keep your hand straight up and down. Tilting or rotating your will cause the gesture recognizer to unrecognize your hand gesture.

### Moving mouse

To move the mouse, move your hand into view of your camera and make an open palm gesture like this 🖐️. The mouse on screen will match your hand's movement. The hand tracker uses the base of your middle finger to track your hand's movement so imagine you're moving the mouse with the middle of your hand to get the best feeling for moving the mouse.

### Clicking

For all types of clicks, the mouse will only click once even if you keep your hand in the same clicking gesture. To click again, make any other gesture then make the desired click's gesture again.

### Left Click

To left click, make a pointing up gesture like this ☝️. 

### Right Click

To right click, make a peace sign (same as pointing up but with middle finger pointing up as well) like this ✌️.

### Middle Click

To middle click, make a fist like this ✊.

### Dragging

To click and drag, move the mouse to one point of where you want to start dragging. Then make spiderman gesture (I love you in sign language) like this 🤟. Keep your hand in this gesture and move your hand to move the mouse into the opposite point of where you want the dragging to end. Once you do any other gesture, the mouse will drag from the start to end points.

### Scrolling

To scroll up, make a thumbs up like this 👍. Unsurprisingly, to scroll down, make a thumbs down like this 👎.

