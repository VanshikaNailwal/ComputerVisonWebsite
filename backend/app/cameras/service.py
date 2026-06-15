from fastapi import HTTPException


from sqlalchemy.orm import Session


from app.cameras.models import Camera


import cv2










# ----------------------------------
# Create Camera
# ----------------------------------

def create_camera(

    db: Session,

    data,

    current_user

):



    existing_ip = db.query(

        Camera

    ).filter(

        Camera.ip_address == data.ip_address

    ).first()



    if existing_ip:


        raise HTTPException(

            status_code=400,

            detail="Camera IP already exists"

        )








    existing_rtsp = db.query(

        Camera

    ).filter(

        Camera.rtsp_url == data.rtsp_url

    ).first()




    if existing_rtsp:


        raise HTTPException(

            status_code=400,

            detail="RTSP URL already exists"

        )










    camera = Camera(


        name=data.name,


        ip_address=data.ip_address,


        location=data.location,


        rtsp_url=data.rtsp_url,


        status="ACTIVE",


        # new camera starts checking
        connection_status="CHECKING",


        created_by=current_user.id


    )







    db.add(

        camera

    )


    db.commit()



    db.refresh(

        camera

    )






    return camera

















# ----------------------------------
# Get All Cameras
# ----------------------------------

def get_all_cameras(

    db: Session

):


    return db.query(

        Camera

    ).all()















# ----------------------------------
# Get Camera By ID
# ----------------------------------

def get_camera_by_id(

    db: Session,

    camera_id

):



    camera = db.query(

        Camera

    ).filter(

        Camera.id == camera_id

    ).first()






    if not camera:



        raise HTTPException(

            status_code=404,

            detail="Camera not found"

        )





    return camera















# ----------------------------------
# Update Camera
# ----------------------------------

def update_camera(

    db: Session,

    camera_id,

    data

):



    camera = get_camera_by_id(

        db,

        camera_id

    )







    if data.name is not None:


        camera.name=data.name








    if data.ip_address is not None:



        duplicate=db.query(

            Camera

        ).filter(

            Camera.ip_address == data.ip_address,

            Camera.id != camera_id

        ).first()




        if duplicate:


            raise HTTPException(

                status_code=400,

                detail="IP already assigned"

            )




        camera.ip_address=data.ip_address










    if data.location is not None:


        camera.location=data.location










    if data.rtsp_url is not None:


        camera.rtsp_url=data.rtsp_url



        # force recheck

        camera.connection_status="CHECKING"










    if data.status is not None:



        camera.status=data.status











    db.commit()



    db.refresh(

        camera

    )





    return camera

















# ----------------------------------
# Delete Camera
# ----------------------------------

def delete_camera(

    db: Session,

    camera_id

):



    camera=get_camera_by_id(

        db,

        camera_id

    )





    db.delete(

        camera

    )



    db.commit()






    return {

        "message":"Camera deleted successfully"

    }
















# ----------------------------------
# Test Camera Connection
# Manual Test Button
# ----------------------------------

def test_camera_connection(

    db:Session,

    camera_id

):



    camera=get_camera_by_id(

        db,

        camera_id

    )







    try:


        camera.connection_status="CHECKING"



        db.commit()







        cap=cv2.VideoCapture(

            camera.rtsp_url

        )





        success=False








        # try few frames

        for _ in range(5):



            ret,frame=cap.read()




            if ret and frame is not None:



                success=True



                break







        cap.release()









        if success:


            camera.connection_status="ONLINE"



        else:


            camera.connection_status="OFFLINE"









        db.commit()



        db.refresh(

            camera

        )









        return {


            "camera":camera.name,


            "connection_status":camera.connection_status


        }











    except Exception:



        camera.connection_status="OFFLINE"




        db.commit()



        db.refresh(

            camera

        )






        return {


            "camera":camera.name,


            "connection_status":"OFFLINE"


        }
