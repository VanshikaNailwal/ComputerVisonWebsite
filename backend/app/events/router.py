from uuid import UUID


from datetime import datetime, timezone


from fastapi import (

    APIRouter,

    Depends,

    HTTPException,

    Query

)


from sqlalchemy.orm import Session



from app.database import get_db


from app.events.models import Event


from app.events.schemas import (

    EventResponse,

    EventStatusUpdate

)










# ----------------------------------
# Router
# ----------------------------------

router = APIRouter(

    prefix="/events",

    tags=["Events"]

)









# ----------------------------------
# Format Event Response
# ----------------------------------

def format_event(event):


    return {


        "id": event.id,


        "camera_id": event.camera_id,


        "camera_name": (

            event.camera.name

            if event.camera

            else "Unknown Camera"

        ),



        "model_id": event.model_id,


        "model_name": (

            event.ai_model.name

            if event.ai_model

            else "Unknown Model"

        ),



        "label": event.event_type,


        "confidence": event.confidence,


        "image_path": event.image_path,



        "status": event.status,


        "resolution_note": event.resolution_note,


        "resolved_by": event.resolved_by,


        "resolved_at": event.resolved_at,



        "created_at": event.created_at


    }









# ----------------------------------
# Get Events With Pagination
#
# GET:
# /events?page=1&limit=20
# ----------------------------------

@router.get("")
def get_events(


    page:int = Query(

        1,

        ge=1

    ),



    limit:int = Query(

        20,

        ge=1,

        le=100

    ),




    db:Session = Depends(get_db)


):



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

            (page-1)*limit

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


        "data":[


            format_event(event)


            for event in events


        ]


    }












# ----------------------------------
# Get Single Event
# ----------------------------------

@router.get(

    "/{event_id}",

    response_model=EventResponse

)

def get_event(


    event_id:UUID,


    db:Session=Depends(get_db)

):



    event = (

        db.query(Event)

        .filter(

            Event.id == event_id

        )

        .first()

    )







    if not event:


        raise HTTPException(

            status_code=404,

            detail="Event not found"

        )








    return format_event(

        event

    )












# ----------------------------------
# Update Status
# ----------------------------------

@router.patch(

    "/{event_id}/status",

    response_model=EventResponse

)

def update_event_status(


    event_id:UUID,


    data:EventStatusUpdate,


    db:Session=Depends(get_db)

):



    event = (

        db.query(Event)

        .filter(

            Event.id == event_id

        )

        .first()

    )







    if not event:


        raise HTTPException(

            status_code=404,

            detail="Event not found"

        )









    allowed_status=[

        "ACTIVE",

        "RESOLVED",

        "FALSE ALARM"

    ]






    if data.status not in allowed_status:


        raise HTTPException(

            status_code=400,

            detail="Invalid status"

        )









    if(

        data.status!="ACTIVE"

        and

        not data.resolution_note.strip()

    ):


        raise HTTPException(

            status_code=400,

            detail="Resolution note required"

        )










    event.status=data.status








    if data.status=="ACTIVE":


        event.resolution_note=None


        event.resolved_by=None


        event.resolved_at=None





    else:


        event.resolution_note=data.resolution_note


        event.resolved_by=data.resolved_by


        event.resolved_at=datetime.now(

            timezone.utc

        )









    db.commit()



    db.refresh(event)








    return format_event(event)













# ----------------------------------
# Delete Event
# ----------------------------------

@router.delete(

    "/{event_id}"

)

def delete_event(


    event_id:UUID,


    db:Session=Depends(get_db)

):



    event=(

        db.query(Event)

        .filter(

            Event.id==event_id

        )

        .first()

    )








    if not event:


        raise HTTPException(

            status_code=404,

            detail="Event not found"

        )









    db.delete(event)


    db.commit()








    return {


        "message":"Event deleted"


    }