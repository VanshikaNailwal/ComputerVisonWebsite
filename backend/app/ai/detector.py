from ultralytics import YOLO


import logging





# ----------------------------------
# Logger
# ----------------------------------

logger = logging.getLogger(

    __name__

)









# ----------------------------------
# Loaded AI Models Cache
# ----------------------------------

loaded_models = {}









# ----------------------------------
# Load Model Once
# ----------------------------------

def get_model(

    model_path

):



    if model_path not in loaded_models:



        logger.info(

            f"Loading AI model: {model_path}"

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
# Run Detection
# ----------------------------------

def detect_objects(

    frame,

    model_path

):



    model = get_model(

        model_path

    )






    # ----------------------------------
    # YOLO inference
    # verbose=False removes frame logs
    # ----------------------------------

    results = model(

        frame,


        verbose=False

    )









    detections = []









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


                    "label":label,


                    "confidence":round(

                        confidence,

                        2

                    )


                }


            )









    return detections