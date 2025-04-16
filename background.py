import cv2

cap = cv2.VideoCapture(0)
print("Stand aside — capturing background. Press 'q' when ready.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Background Capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("image.jpg", frame)
        print("Background saved as image.jpg")
        break

cap.release()
cv2.destroyAllWindows()
