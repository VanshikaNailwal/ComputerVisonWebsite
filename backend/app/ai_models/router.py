from pathlib import Path


from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException
)


from sqlalchemy.orm import Session


import shutil


from ultralytics import YOLO



from app.database import get_db


from app.ai_models.models import AIModel


from app.events.models import Event


from app.core.config import settings







# ----------------------------------
# Router
# ----------------------------------

router = APIRouter(

    prefix="/models",

    tags=["AI Models"]

)









# ----------------------------------
# Dynamic Model Directory
#
# Comes from:
# storage_config.txt
# selected during install
# ----------------------------------

MODEL_DIR = Path(

    settings.MODEL_PATH

)



MODEL_DIR.mkdir(

    parents=True,

    exist_ok=True

)










# ----------------------------------
# Upload AI Model
# ----------------------------------

@router.post("/upload")
async def upload_model(


    name: str = Form(...),


    usecase: str = Form(...),


    version: str = Form(...),


    file: UploadFile = File(...),


    db: Session = Depends(get_db)


):




    # ------------------------------
    # Validate extension
    # ------------------------------

    if not file.filename.endswith(".pt"):


        raise HTTPException(

            status_code=400,

            detail="Only .pt model files allowed"

        )









    # ------------------------------
    # Duplicate check
    # ------------------------------

    existing = (

        db.query(

            AIModel

        )


        .filter(

            AIModel.filename == file.filename

        )


        .first()

    )






    if existing:


        raise HTTPException(

            status_code=400,

            detail="Model already uploaded"

        )









    # ------------------------------
    # Save Model File
    # ------------------------------

    save_path = (

        MODEL_DIR

        /

        file.filename

    )





    with open(

        save_path,

        "wb"

    ) as buffer:



        shutil.copyfileobj(

            file.file,

            buffer

        )









    # ------------------------------
    # Create DB Entry
    # ------------------------------

    new_model = AIModel(


        name=name,


        usecase=usecase,


        version=version,


        filename=file.filename,


        # only store filename
        # not absolute path

        file_path=file.filename,


        status="CHECKING"


    )







    db.add(

        new_model

    )


    db.commit()


    db.refresh(

        new_model

    )










    # ------------------------------
    # Validate YOLO Model
    # ------------------------------

    try:


        YOLO(

            str(save_path)

        )


        new_model.status = "READY"




    except Exception:


        new_model.status = "FAILED"







    db.commit()


    db.refresh(

        new_model

    )










    return {


        "message": "Model uploaded successfully",


        "id": new_model.id,


        "name": new_model.name,


        "usecase": new_model.usecase,


        "version": new_model.version,


        "filename": new_model.filename,


        "path": new_model.file_path,


        "status": new_model.status


    }













# ----------------------------------
# Get All AI Models
# ----------------------------------

@router.get("")
def get_models(


    db: Session = Depends(get_db)


):


    models = (

        db.query(

            AIModel

        )

        .all()

    )








    return [


        {


            "id": model.id,


            "name": model.name,


            "usecase": model.usecase,


            "version": model.version,


            "filename": model.filename,


            "path": model.file_path,


            "status": model.status


        }


        for model in models


    ]













# ----------------------------------
# Delete AI Model
# ----------------------------------

@router.delete("/{model_id}")
def delete_model(


    model_id: int,


    db: Session = Depends(get_db)


):




    model = (

        db.query(

            AIModel

        )


        .filter(

            AIModel.id == model_id

        )


        .first()

    )








    if not model:


        raise HTTPException(

            status_code=404,

            detail="Model not found"

        )








    # ------------------------------
    # Remove model references
    # from existing alerts
    #
    # Keeps evidence history
    # ------------------------------

    db.query(

        Event

    ).filter(

        Event.model_id == model.id

    ).update(

        {

            Event.model_id: None

        }

    )










    # ------------------------------
    # Delete physical .pt file
    # ------------------------------

    file_path = (

        MODEL_DIR

        /

        model.filename

    )




    if file_path.exists():


        file_path.unlink()










    # ------------------------------
    # Delete database row
    # ------------------------------

    db.delete(

        model

    )


    db.commit()










    return {


        "message": "Model deleted successfully"


    }