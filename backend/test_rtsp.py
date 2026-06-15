import os

import cv2



# Force OpenCV RTSP TCP mode

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (

    "rtsp_transport;tcp"

)





# ============================
# CAMERA LIST
# ============================


cameras = {


    "Camera 1 - Webcam":

        "rtsp://127.0.0.1:8554/camera1",



    "Camera 2 - Fire Video":

        "rtsp://127.0.0.1:8555/camera2"


}







# ============================
# TEST FUNCTION
# ============================


def test_camera(name, url):



    print("\n==============================")

    print("Testing:", name)

    print(url)

    print("==============================")




    cap = cv2.VideoCapture(

        url,

        cv2.CAP_FFMPEG

    )




    cap.set(

        cv2.CAP_PROP_OPEN_TIMEOUT_MSEC,

        5000

    )



    cap.set(

        cv2.CAP_PROP_READ_TIMEOUT_MSEC,

        5000

    )




    ret, frame = cap.read()




    if ret:


        print(

            "ONLINE ✅"

        )


        print(

            "Frame size:",

            frame.shape

        )



    else:


        print(

            "OFFLINE ❌"

        )




    cap.release()








# ============================
# RUN TESTS
# ============================


for name, url in cameras.items():


    test_camera(

        name,

        url

    )




print(

    "\nCamera testing finished"

)