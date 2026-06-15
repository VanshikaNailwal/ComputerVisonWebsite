import os

import cv2



# Force RTSP TCP mode

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
    "rtsp_transport;tcp"
)




url = "rtsp://127.0.0.1:8554/test"




cap = cv2.VideoCapture(

    url,

    cv2.CAP_FFMPEG

)




if not cap.isOpened():


    print("Camera stream not opened")


    exit()




print("Camera connected successfully")

print("Starting frame extraction...")




frame_count = 0



while True:



    ret, frame = cap.read()



    if not ret:


        print("Frame not received")


        break




    frame_count += 1



    print(

        "Frame extracted:",

        frame_count,

        frame.shape

    )




    cv2.imshow(

        "HMEL Camera Stream",

        frame

    )




    # press q to stop

    if cv2.waitKey(1) & 0xFF == ord("q"):


        break




cap.release()


cv2.destroyAllWindows()



print("Stream closed")