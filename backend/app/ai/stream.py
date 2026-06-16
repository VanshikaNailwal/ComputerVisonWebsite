import os

import cv2

import time

import logging



from app.database import SessionLocal

from app.cameras.models import Camera

from app.ai.detector import detect_objects

from app.events.service import create_event

from app.core.config import settings








# ----------------------------------
# Logger
# ----------------------------------

logger = logging.getLogger(

    __name__

)










# ----------------------------------
# AI Settings
# ----------------------------------

FRAME_SKIP = settings.FRAME_SKIP


CONFIDENCE_THRESHOLD = settings.CONFIDENCE_THRESHOLD


ALERT_COOLDOWN = settings.ALERT_COOLDOWN










# ----------------------------------
# Process Camera Stream
# ----------------------------------

def process_camera(

    camera_id,

    stop_flags

):


    db = SessionLocal()


    cap = None


    frame_count = 0


    last_alert_time = {}









    try:



        # ------------------------------
        # Load Camera
        # ------------------------------

        camera = (

            db.query(

                Camera

            )


            .filter(

                Camera.id == camera_id

            )


            .first()

        )








        if not camera:


            logger.error(

                "Camera not found"

            )


            return











        # ------------------------------
        # Load Models
        # ------------------------------

        mapped_models = [

            mapping.ai_model

            for mapping in camera.model_mappings

        ]








        if not mapped_models:


            logger.warning(

                f"No models mapped for {camera.name}"

            )


            return










        logger.info(

            f"AI Started: {camera.name}"

        )



        logger.info(

            f"Models: {[m.name for m in mapped_models]}"

        )









        # ------------------------------
        # Prepare Model Paths ONCE
        # ------------------------------

        prepared_models = []




        for model in mapped_models:



            filename = os.path.basename(

                model.file_path

            )



            path = os.path.join(

                settings.MODEL_PATH,

                filename

            )




            logger.info(

                f"Loading AI model: {path}"

            )




            prepared_models.append(

                {

                    "model": model,

                    "path": path

                }

            )











        # ------------------------------
        # Open Camera Stream
        # ------------------------------

        cap = cv2.VideoCapture(

            camera.rtsp_url

        )








        if not cap.isOpened():


            logger.error(

                f"Unable to open camera {camera.name}"

            )


            return










        failed_frames = 0











        # ------------------------------
        # Frame Loop
        # ------------------------------

        while True:




            camera_key = str(

                camera_id

            )







            if stop_flags.get(

                camera_key,

                False

            ):


                logger.info(

                    f"AI stopped: {camera.name}"

                )


                break











            success, frame = cap.read()









            if not success or frame is None:



                failed_frames += 1




                if failed_frames >= 30:


                    logger.error(

                        f"Camera disconnected: {camera.name}"

                    )


                    break




                continue










            failed_frames = 0


            frame_count += 1










            if frame_count % FRAME_SKIP != 0:


                continue











            # ------------------------------
            # Detection
            # ------------------------------

            for item in prepared_models:




                model = item["model"]


                model_path = item["path"]







                detections = detect_objects(

                    frame,

                    model_path

                )









                for detection in detections:








                    if detection["confidence"] < CONFIDENCE_THRESHOLD:


                        continue









                    key = (

                        f"{model.id}_{detection['label']}"

                    )




                    current = time.time()










                    if key in last_alert_time:


                        if (

                            current

                            -

                            last_alert_time[key]

                            <

                            ALERT_COOLDOWN

                        ):


                            continue








                    last_alert_time[key] = current










                    event = create_event(


                        db=db,


                        camera_id=camera.id,


                        model_id=model.id,


                        detection=detection,


                        frame=frame

                    )










                    if event:


                        logger.info(

                            f"ALERT CREATED | "
                            f"{camera.name} | "
                            f"{model.name} | "
                            f"{detection['label']} | "
                            f"{detection['confidence']}"

                        )










        logger.info(

            f"AI ended: {camera.name}"

        )









    except Exception as e:


        logger.exception(

            f"AI Stream Error: {e}"

        )










    finally:



        if cap:


            cap.release()







        db.close()








        logger.info(

            f"Released resources: {camera_id}"

        )