from fastapi import (

    APIRouter,
    Depends

)


from sqlalchemy.orm import Session


from sqlalchemy import func



from app.database import get_db



from app.cameras.models import Camera


from app.ai_models.models import AIModel


from app.events.models import Event


from app.users.models import User







# ----------------------------------
# Router
# ----------------------------------

router = APIRouter(

    prefix="/dashboard",

    tags=["Dashboard"]

)









# ==================================
# ADMIN DASHBOARD
# ==================================

@router.get("/admin")
def admin_dashboard(

    db:Session = Depends(get_db)

):



    # -----------------------------
    # Cameras
    # -----------------------------

    total_cameras = db.query(

        Camera

    ).count()






    online_cameras = db.query(

        Camera

    ).filter(

        Camera.connection_status=="ONLINE"

    ).count()






    offline_cameras = db.query(

        Camera

    ).filter(

        Camera.connection_status=="OFFLINE"

    ).count()









    # -----------------------------
    # AI Models
    # -----------------------------

    total_models = db.query(

        AIModel

    ).count()










    # -----------------------------
    # Users
    # -----------------------------

    total_users = db.query(

        User

    ).count()











    # -----------------------------
    # Alerts
    # -----------------------------

    total_alerts = db.query(

        Event

    ).count()






    active_alerts = db.query(

        Event

    ).filter(

        Event.status=="ACTIVE"

    ).count()








    resolved_alerts = db.query(

        Event

    ).filter(

        Event.status=="RESOLVED"

    ).count()







    false_alerts = db.query(

        Event

    ).filter(

        Event.status=="FALSE ALARM"

    ).count()










    # -----------------------------
    # Recent Alerts
    # -----------------------------

    recent = db.query(

        Event

    ).order_by(

        Event.created_at.desc()

    ).limit(

        5

    ).all()









    return {


        "cameras":{

            "total":total_cameras,

            "online":online_cameras,

            "offline":offline_cameras

        },


        "models":{

            "total":total_models

        },


        "users":{

            "total":total_users

        },


        "alerts":{


            "total":total_alerts,


            "active":active_alerts,


            "resolved":resolved_alerts,


            "false_alarm":false_alerts

        },



        "recent_alerts":[

            {

                "id":x.id,

                "camera":x.camera.name if x.camera else None,

                "model":x.ai_model.name if x.ai_model else None,

                "type":x.event_type,

                "status":x.status,

                "time":x.created_at


            }

            for x in recent

        ]

    }














# ==================================
# OPERATOR DASHBOARD
# ==================================

@router.get("/operator")
def operator_dashboard(

    db:Session = Depends(get_db)

):





    active_alerts=db.query(

        Event

    ).filter(

        Event.status=="ACTIVE"

    ).count()








    resolved=db.query(

        Event

    ).filter(

        Event.status=="RESOLVED"

    ).count()











    false_alarm=db.query(

        Event

    ).filter(

        Event.status=="FALSE ALARM"

    ).count()











    recent=db.query(

        Event

    ).filter(

        Event.status=="ACTIVE"

    ).order_by(

        Event.created_at.desc()

    ).limit(

        10

    ).all()











    return {


        "summary":{


            "active":active_alerts,


            "resolved":resolved,


            "false_alarm":false_alarm

        },



        "active_alerts":[


            {

                "id":x.id,


                "camera":x.camera.name if x.camera else None,


                "model":x.ai_model.name if x.ai_model else None,


                "type":x.event_type,


                "confidence":x.confidence,


                "image":x.image_path,


                "time":x.created_at



            }

            for x in recent

        ]

    }