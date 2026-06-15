import cv2


cap = cv2.VideoCapture(0)


ret, frame = cap.read()


if ret:

    print("CAMERA WORKING")
    print(frame.shape)

else:

    print("FAILED")


cap.release()