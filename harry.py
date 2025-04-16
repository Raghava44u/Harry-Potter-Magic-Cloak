import cv2
import numpy as np

cap = cv2.VideoCapture(0)

background = cv2.imread('./image.jpg')
if background is None:
    print("Couldn't load background image (image.jpg).")
    exit()

ret, current_frame = cap.read()
if not ret:
    print("Webcam error.")
    cap.release()
    exit()

background = cv2.resize(background, (current_frame.shape[1], current_frame.shape[0]))

cv2.namedWindow("Cloak Magic", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Cloak Magic", 800, 600)

while cap.isOpened():
    ret, current_frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

    l_red1 = np.array([0, 100, 100])
    u_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, l_red1, u_red1)

    l_red2 = np.array([170, 100, 100])
    u_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, l_red2, u_red2)

    red_mask = mask1 + mask2

    lower_skin = np.array([0, 20, 70])
    upper_skin = np.array([20, 255, 255])
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

    red_mask = cv2.bitwise_and(red_mask, red_mask, mask=cv2.bitwise_not(skin_mask))

    kernel = np.ones((15, 15), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_DILATE, kernel, iterations=1)

    part1 = cv2.bitwise_and(background, background, mask=red_mask)
    red_free = cv2.bitwise_not(red_mask)
    part2 = cv2.bitwise_and(current_frame, current_frame, mask=red_free)

    output = cv2.addWeighted(part1, 1, part2, 1, 0)

    output_resized = cv2.resize(output, (800, 600))

    cv2.imshow("Cloak Magic", output_resized)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r') or key == 27 or cv2.getWindowProperty("Cloak Magic", cv2.WND_PROP_VISIBLE) < 1:
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
