import cv2
from ultralytics import YOLO


def process_camera(camera):

    cap = cv2.VideoCapture(
        camera.rtsp_url
    )


    model = YOLO(
        camera.model_path
    )


    while True:

        success, frame = cap.read()

        if not success:
            break


        results = model(frame)


        for r in results:

            boxes = r.boxes

            for box in boxes:

                cls = int(box.cls[0])
                conf = float(box.conf[0])

                print(
                    cls,
                    conf
                )