# Air Mouse

Air Mouse lets you control your mouse using your camera to track your hand and recognize hand gestures. The mouse matches the movement of your hand and the recognized hand gestures control different mouse functions like left and right click.

## How to Install

To begin, you must have **Python version 3.10** installed. You can either downgrade/upgrade your Python version to match this version or create a virtual environment with Python 3.10.
Next, you will have to install four libraries: OpenCV, MediaPipe, mouse and pywin32. OpenCV is a powerful computer vision library however the only feature used here is accessing the camera. MediaPipe is a library that utilizes artificial intelligence and machine learning for a wide range of solutions, but this project will only use the hand tracking and gesture recognition solutions. mouse is a library that allows you to programmatically control your mouse. pywin32 provides access to tons of Python 3 Windows APIS but this library will only be used to retrieve the screen's resolution with the scaling percentage.

### Libraries

To install OpenCV, run the following command in your command line:

```
python -m pip install opencv
```

To install MediaPipe, run the following command in your command line:

```
python -m pip install mediapipe
```

To install mouse, run the following command in your command line:

```
python -m pip install mouse
```

To install pywin32, run the following command in your command line:

```
python -m pip install pywin32
```

Now that you have the correct version of Python and the libraries installed, you're good to download this project's code and run the code in your programming environment.

## How to use

To get the best results for all hand gestures, orientate your hand so your palm is facing the camera and keep your hand straight up and down. Tilting or rotating your can cause the gesture recognizer to unrecognize your hand gesture.

### Mouse Movement

- MOVING MOUSE

  To move the mouse, move your hand into view of your camera and make an open palm gesture like this 🖐️. The mouse on screen will match your hand's movement. The hand tracker uses the base of your middle finger to track your hand's movement so imagine you're moving the mouse with the middle of your hand to get the best feeling for moving the mouse.

- DRAGGING

  To click and drag, move the mouse to one point of where you want to start dragging. Then make spiderman gesture (I love you in sign language) like this 🤟. Keep your hand in this gesture and move your hand to move the mouse into the opposite point of where you want the dragging to end. Once you do any other gesture, the mouse will drag from the start to end points.

- MOVING MOUSE SLOWLY

  To move the mouse more slowly, tilt your hand forward towards the camera. You may have to move your hand closer to the camera. For best results, if having your palm facing the camera straight up and down is 0 degrees, tilt your hand forward about 35 degrees. To return to regular mouse movement speed, return your hand to an upright position. Moving the mouse slowly is possible both during regular mouse movement and dragging.

### Clicking

For all types of clicks, the mouse will only click once even if you keep your hand in the same clicking gesture. To click again, make any other gesture then make the desired click's gesture again.

- LEFT CLICK

  To left click, make a pointing up gesture like this ☝️.

- RIGHT CLICK

  To right click, make a peace sign (same as pointing up but with middle finger pointing up as well) like this ✌️.

- MIDDLE CLICK

  To middle click, make a fist like this ✊.

### Scrolling

To scroll up, make a thumbs up like this 👍. Unsurprisingly, to scroll down, make a thumbs down like this 👎.

## Logic Explained

In the main file, there are comments explaining the code but some of those explanations are too long to reasonably be in the file so they will be explained here.

### JITTERY MOUSE PREVENTION

Hand coordinates are stored with 17 decimal places. The micro jumping between these barely different coordinate values makes the mouse jitter on the screen. To prevent this, the difference between the hand position in the previous frame and the hand position in the current frame must be above a threshold to actually move the mouse.

### MOVE MOUSE FUNCTION

For regular mouse movement, the move function takes in x and y pixel coordinates to move the mouse to that pixel on screen. The coordinates being fed to the function are the coordinates from the middle finger knuckle landmark. However, the landmark coordinates are on a scale of 0-1 with 0 and 1 being the edges of the camera feed. This means the landmark coordinates must be multiplied by the pixel dimensions of the screen to be on the scale that the function can use. Additionaly, the hand tracking cuts in and out when a hand is at the edge of the camera feed so it is hard to control the mouse near the edge of the screen. To prevent this, a simple formula is being applied to the landmark coordinates before being multiplied by the pixel dimensions. This formula makes the mouse reach the edges of the screen at about 0.2 and 0.8 on the landmark scale (usually 0 and 1) while keeping 0.5 as the center of the screen. This way a hand does not have to reach the edges of the camera feed to move the mouse to the edges of the screen.

### PRECISE MOVE MOUSE FUNCTION

For precise mouse movement, the mouse must move relative to the mouse's location when precise mouse movement is initiated. This means the hand landmark coordinates cannot just be mapped to the screens dimensions like in the regular mouse move function. Instead the precise move function takes in a a numbers of pixels to move in the x direction and a number of pixels to move in the y direction. This pixel distance is calculated by finding the difference between the hand landmark coordinates in the last frame and the hand landmark coordinates of the current frame. Similarly to the regular move mouse function, these values must be multiplied because the hand landmark coordinates are on a 0-1 scale. However, the values are multiplied by much less than in the move mouse function making the movement of the mouse much more precise.

### PRECISE FRAME BUFFER

The hand landmark z coordinate (the distance of the wrist to the camera) fluctuates greatly between frames. Because of this, the z coordinate will often rise above the precise movement threshold for a few frames during precise movement. To prevent exiting precise mouse movement mode unintentionally, the z coordinate must be above the precise movement threshold for a set number of consecutive frames. If this condition is met, then the user is most likely intentionally pulling their hand back to exit precise movement mode.
