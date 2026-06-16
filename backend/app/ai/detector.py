from pathlib import Path


from ultralytics import YOLO


import logging







# ----------------------------------
# Logger
# ----------------------------------

logger = logging.getLogger(

    __name__

)










# ----------------------------------
# Loaded Models Cache
# path -> YOLO object
# ----------------------------------

loaded_models = {}









# ----------------------------------
# Load YOLO Model Once
# ----------------------------------

def get_model(

    model_path

):



    model_path = str(

        Path(

            model_path

        ).resolve()

    )







    # ------------------------------
    # Check model exists
    # ------------------------------

    if not Path(

        model_path

    ).exists():



        raise FileNotFoundError(

            f"AI model missing: {model_path}"

        )









    # ------------------------------
    # Load only first time
    # ------------------------------

    if model_path not in loaded_models:



        logger.info(

            f"Loading AI model once: {model_path}"

        )




        loaded_models[

            model_path

        ] = YOLO(

            model_path

        )







    return loaded_models[

        model_path

    ]












# ----------------------------------
# Run Object Detection
# ----------------------------------

def detect_objects(

    frame,

    model_path

):



    model = get_model(

        model_path

    )









    # ------------------------------
    # YOLO Inference
    # ------------------------------

    results = model(

        frame,

        verbose=False

    )









    detections = []









    # ------------------------------
    # Parse Results
    # ------------------------------

    for result in results:




        for box in result.boxes:





            cls_id = int(

                box.cls[0]

            )






            confidence = float(

                box.conf[0]

            )






            label = model.names[

                cls_id

            ]










            detections.append(


                {


                    "label": label,


                    "confidence": round(

                        confidence,

                        2

                    )


                }


            )








    return detections