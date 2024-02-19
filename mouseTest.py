import mouse
import time

# left click
# mouse.click('right')

# drag from (0, 0) to (100, 100) relatively with a duration of 0.1s
# mouse.drag(0, 0, 100, 0, absolute=False, duration=0.1)

# move 100 right & 100 down
# mouse.move(3000, 2000, absolute=True, duration=0.2)
while (True):
    print(mouse.get_position())
    time.sleep(0.5)
