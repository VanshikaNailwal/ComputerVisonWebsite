import os


import cv2


import logging


from datetime import datetime



from app.events.models import Event


from app.core.config import settings








# ----------------------------------
# Logger
# ----------------------------------

logger = logging.getLogger(

    __name__

)









# ----------------------------------
# Create AI Detection Event
# Called from AI stream
# ----------------------------------

def create_event(

    db,

    camera_id,

    model_id,

    detection=None,

    event_type=None,

    confidence=None,

    image_path=None,

    frame=None,

    **kwargs

):



    # ------------------------------
    # Handle detection dictionary
    # ------------------------------

    if detection:


        event_type = detection.get(

            "label",

            detection.get(

                "class",

                "UNKNOWN"

            )

        )



        confidence = detection.get(

            "confidence",

            0

        )



        image_path = detection.get(

            "image_path",

            image_path

        )









    # ------------------------------
    # Save Evidence Image From Frame
    # ------------------------------

    if frame is not None:



        logger.info(

            "Saving evidence image"

        )





        folder = settings.EVIDENCE_PATH





        os.makedirs(

            folder,

            exist_ok=True

        )









        filename = (

            str(event_type)

            +

            "_"

            +

            datetime.now().strftime(

                "%Y%m%d_%H%M%S_%f"

            )

            +

            ".jpg"

        )











        save_path = os.path.join(

            folder,

            filename

        )











        saved = cv2.imwrite(

            save_path,

            frame

        )











        logger.info(

            f"IMAGE PATH: {save_path}"

        )



        logger.info(

            f"IMAGE SAVED: {saved}"

        )









        if saved:


            image_path = (

                "storage/evidence/"

                +

                filename

            )













    # ------------------------------
    # Save Event In Database
    # ------------------------------

    event = Event(


        camera_id=camera_id,


        model_id=model_id,


        event_type=event_type,


        confidence=confidence,


        image_path=image_path,


        status="ACTIVE"


    )










    db.add(

        event

    )



    db.commit()



    db.refresh(

        event

    )









    return event















# ----------------------------------
# Pagination for Alerts Page
# ----------------------------------

def get_events_paginated(

    db,

    page:int = 1,

    limit:int = 20

):




    skip = (

        page - 1

    ) * limit









    total = db.query(

        Event

    ).count()









    events = (

        db.query(

            Event

        )


        .order_by(

            Event.created_at.desc()

        )


        .offset(

            skip

        )


        .limit(

            limit

        )


        .all()

    )











    return {


        "total":total,


        "page":page,


        "limit":limit,


        "data":events


    }
















# ----------------------------------
# Delete Event
# ----------------------------------

def delete_event_by_id(

    db,

    event_id

):




    event = (

        db.query(

            Event

        )


        .filter(

            Event.id == event_id

        )


        .first()

    )











    if not event:


        return False












    db.delete(

        event

    )




    db.commit()










    return True