from fastapi import HTTPException


from sqlalchemy.orm import Session



from app.cameras.models import Camera


from app.ai_models.models import AIModel


from app.mapping.models import CameraModelMapping












# ----------------------------------
# Create / Update Mapping
# ----------------------------------

def create_mapping(

    db: Session,

    data

):



    # check camera exists

    camera = db.query(

        Camera

    ).filter(

        Camera.id == data.camera_id

    ).first()







    if not camera:


        raise HTTPException(

            status_code=404,

            detail="Camera not found"

        )









    # remove previous mappings for this camera

    db.query(

        CameraModelMapping

    ).filter(

        CameraModelMapping.camera_id == data.camera_id

    ).delete()










    # add new mappings

    for model_id in data.model_ids:




        model = db.query(

            AIModel

        ).filter(

            AIModel.id == model_id

        ).first()







        if not model:


            raise HTTPException(

                status_code=404,

                detail=f"Model {model_id} not found"

            )









        mapping = CameraModelMapping(

            camera_id=data.camera_id,

            model_id=model_id

        )






        db.add(

            mapping

        )









    db.commit()







    return {

        "message":

        "Mapping saved successfully"

    }














# ----------------------------------
# Get All Mappings
# ----------------------------------

def get_all_mappings(

    db: Session

):




    cameras = db.query(

        Camera

    ).all()








    result=[]








    for camera in cameras:





        result.append(

            {

                "camera_id": camera.id,


                "camera_name": camera.name,


                "models": [

                    {

                        "id": item.ai_model.id,


                        "name": item.ai_model.name,


                        "filename": item.ai_model.filename

                    }


                    for item in camera.model_mappings

                ]

            }

        )








    return result















# ----------------------------------
# Delete Mapping For Camera
# ----------------------------------

def delete_mapping(

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









    db.query(

        CameraModelMapping

    ).filter(

        CameraModelMapping.camera_id == camera_id

    ).delete()







    db.commit()







    return {

        "message":

        "Mapping deleted successfully"

    }